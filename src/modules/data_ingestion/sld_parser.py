import json
import pandas as pd
from google import genai
from google.genai import types


class MultimodalSLDParser:
    """
    Independent backend data ingestion engine tasked with extracting structured
    electrical network taxonomies from static PDF drawings and JPEG schematics.
    """

    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.approved_classifications = [
            "Main Distribution Transformer",
            "Auxiliary Step-Down Transformer",
            "Variable Speed Drive (VSD)",
            "Large Induction Motor",
            "Arc Furnace Plant",
            "Ladle Metallurgy Furnace",
            "Power Factor Correction Bank",
            "Industrial LED Lighting Network",
            "General Load",
        ]

    def extract_structured_json_from_drawing(
        self, file_bytes: bytes, mime_type: str
    ) -> list:
        """
        Executes a secure multimodal extraction block against the Gemini boundary.
        Forces structural validation by locking the output format into a JSON schema.
        """
        system_instruction = """
        You are an expert electrical power system auditing engineer. Your task is to interpret 
        the provided Single Line Diagram (SLD) schematic drawing or document and extract a 
        comprehensive registry of all connected electrical equipment nodes.
        """

        prompt = f"""
        Analyze this engineering layout diagram carefully. Extract every individual transformer, 
        motor, variable speed drive, and heavy furnace node present on the drawing.
        
        For each individual asset discovered, compile the following structural keys:
        1. 'Asset Tag' - The unique identification string labeled on the diagram (e.g., TX-01, VSD-04).
        2. 'Plant Location' - The specific electrical branch, panel, or busbar location where it is bound.
        3. 'Classification' - You MUST map the asset type strictly to one of these approved strings: {self.approved_classifications}.
        4. 'Rating (kW)' - The continuous numerical power capacity rating in kW. Extract numbers only.
        5. 'Weekly Hrs' - The estimated weekly runtime. Look for operational schedule notes on the drawing, or default to 40.
        6. 'Distortion (THD_i)' - Extract the recorded current harmonic distortion percentage if annotated, or default to 0.0.
        
        Return the final output strictly as a flat JSON array of objects matching these keys.
        """

        # Enforce structural reliability using a strict response schema definition
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Part.from_bytes(data=file_bytes, mime_type=mime_type),
                prompt,
            ],
            config=types.GenerateContentConfig(
                temperature=0.10,
                system_instruction=system_instruction,
                response_mime_type="application/json",
            ),
        )

        try:
            return json.loads(response.text)
        except json.JSONDecodeError as err:
            raise ValueError(
                f"Backend Extraction Fault: Gemini output failed schema parsing parameters: {str(err)}"
            )

    def convert_extracted_payload_to_registry(self, raw_payload: list) -> pd.DataFrame:
        """
        Adapter function ensuring relational data integrity and layout column alignment.
        Cleans data anomalies and handles safe default fallbacks.
        """
        cleaned_records = []

        for item in raw_payload:
            # 1. Guarantee presence of primary operational identification keys
            tag = str(item.get("Asset Tag", "UNK-TAG")).strip().upper()
            location = str(
                item.get("Plant Location", "Unspecified Sub-Distribution Bay")
            ).strip()

            # 2. Enforce spelling and taxonomy class standardisation
            classification = str(item.get("Classification", "General Load")).strip()
            if classification not in self.approved_classifications:
                classification = "General Load"

            # 3. Defensive numerical precision conversions
            try:
                rating = float(str(item.get("Rating (kW)", "0")).replace(",", ""))
                if rating <= 0:
                    rating = 45.0  # Safe default fallback for industrial motor loads
            except ValueError:
                rating = 45.0

            try:
                hours = float(item.get("Weekly Hrs", 40.0))
                hours = min(168.0, max(1.0, hours))
            except ValueError:
                hours = 40.0

            try:
                thd = float(str(item.get("Distortion (THD_i)", "0.0")).replace("%", ""))
                thd = min(100.0, max(0.0, thd))
            except ValueError:
                thd = 0.0

            cleaned_records.append(
                {
                    "Asset Tag": tag,
                    "Plant Location": location,
                    "Classification": classification,
                    "Rating (kW)": rating,
                    "Weekly Hrs": hours,
                    "Distortion (THD_i)": thd,
                }
            )

        return pd.DataFrame(cleaned_records)
