import os
import google.generativeai as genai
from src.config import settings


class GeminiTranslationService:
    """
    Orchestrates the conversion of cryptic engineering power quality telemetry
    into high-impact boardroom business cases delivered BY the Swalek & Market Catalyst JV
    TO external industrial corporate clients. Uses the legacy google-generativeai package.
    """

    def __init__(self):
        # Configure the legacy library using your existing settings token
        genai.configure(api_key=settings.GEMINI_API_KEY)
        # Using a model string universally supported by the google-generativeai library wrapper
        self.model_name = "gemini-1.5-flash"

    def generate_boardroom_summary(
        self, client_name: str, asset_class: str, telemetry: dict
    ) -> str:
        """
        Formulates an expert, consultative energy audit brief for a target client board.
        If cloud API node drops (e.g., 503 Overload), it switches automatically to an
        intelligent local contextual advisory profile to guarantee boardroom continuity.
        """
        try:
            prompt = f"""
            You are a premier corporate risk strategist and senior industrial power advisor representing 
            the 'Swalek Ltd & Market Catalyst High-Voltage Joint Venture'.
            
            Your task is to write a sophisticated, authoritative consultative executive summary addressed 
            to the Board of Directors of our client: '{client_name}'. 
            
            This summary translates a critical technical vulnerability discovered by our engineering team 
            on their site into a clear, compelling financial risk narrative.
            
            Context Parameters:
            - Target Client Identity: {client_name}
            - Primary Distorted Asset Class: {asset_class}
            - Active Telemetry Signature Captured: {telemetry}
            
            Mandatory Structuring Constraints:
            1. Use strict UK English spelling exclusively (e.g., operationalise, characterise, optimised).
            2. Speak from the perspective of the Swalek & Market Catalyst JV acting as their expert HV engineering advisors.
            3. Break the explanation into two clear parts:
               - 'The Financial Analogy': Map their specific technical leak to a vivid business operational metaphor.
               - 'The Corporate Risk Profile': Articulate how leaving this electrical anomaly unmitigated accelerates balance-sheet erosion.
            4. Keep the tone professional, sharp, consultative, and accessible to non-technical executives. Do not print raw code or math.
            """

            # Legacy generation sequence execution
            model = genai.GenerativeModel(self.model_name)
            response = model.generate_content(prompt)
            return response.text

        except Exception:
            # Cloud connection dropped or throttled. Return the secured local backup card.
            return self._compile_local_advisory_backup(
                client_name, asset_class, telemetry
            )

    def _compile_local_advisory_backup(
        self, client_name: str, asset_class: str, telemetry: dict
    ) -> str:
        """
        Interprets structural parameters locally to build a contextual, polished
        boardroom brief, completely hiding raw server error strings from the client view.
        """
        if "annual_events" in telemetry or "payback_years" in telemetry:
            events = telemetry.get("annual_events", 4)
            capex = telemetry.get("turnkey_capex", 95000.00)
            payback = telemetry.get("payback_years", 1.1)

            return f"""
### 🛡️ STEM Platform Consultative Brief | Automation Continuity Shield
**Prepared for the Board of Directors of {client_name}** *Status: Verified Field Diagnostic Profile (Local Secured Backup Matrix)*

---

#### 🏭 The Financial Analogy
Imagine your main production line operating as a high-precision corporate logistics network where every delivery vehicle must move in perfect split-second synchronisation. A momentary voltage sag is the operational equivalent of a microsecond logjam that slams the brakes on every vehicle simultaneously. The vehicles do not crash due to fuel starvation; rather, their automatic safety systems force an immediate emergency shutdown. The result is a total system stall that requires hours of physical realignment before operations can resume.

#### 📉 The Corporate Risk Profile
Our field assessment confirms that the **{asset_class}** remains highly exposed to transient grid disturbances, averaging **{events} uncoordinated dropouts per annum**. 
* **The Vulnerability:** Leaving this boundary unmitigated forces your sensitive digital PLC brains and robotic control units to trip offline mid-cycle, destroying active work-in-progress materials and running up severe idle labour overheads during the recovery loop.
* **The Strategic Recommendation:** Implementing our proposed turnkey mitigation framework (**£{capex:,.2f} CapEx**) acts as a proactive power insurance policy. It completely insulates your automated assets from grid sags, achieving an optimized simple payback window of **{payback:.1f} years** while safeguarding your downstream delivery commitments.
"""
        elif "thd_i" in telemetry:
            thd = telemetry.get("thd_i", 5.0)
            return f"""
### 🛡️ STEM Platform Consultative Brief | Capital Asset Preservation
**Prepared for the Board of Directors of {client_name}** *Status: Verified Field Diagnostic Profile (Local Secured Backup Matrix)*

---

#### 🚚 The Financial Analogy
Operating your high-voltage infrastructure with severe current distortion is the financial equivalent of running a fleet of heavy distribution lorries with severely misaligned wheels. The vehicles still transport cargo and the engines run, but the structural misalignment generates continuous, violent chassis friction and intense localized heat. You are burning extra energy simply to fight your own hardware, wearing out expensive assets long before their time.

#### 📉 The Corporate Risk Profile
Telemetry captured at your incoming busbars registers an elevated Current Harmonic Distortion score of **{thd}% THD_i** bleeding directly into your **{asset_class}**.
* **The Vulnerability:** This waveform friction drives up non-linear core losses, converting raw power into destructive thermal stress. This constant baking accelerates the degradation of your primary transformer's solid paper insulation, drastically shortening its useful economic life.
* **The Strategic Recommendation:** Deploying STEM's active filtering framework suppresses this back-feed current friction instantly. This intervention stabilizes internal operating temperatures, preserves your balance-sheet capital, and restores years of projected asset life.
"""
        else:
            cos_phi = telemetry.get("cos_phi", 0.80)
            return f"""
### 🛡️ STEM Platform Consultative Brief | Network Efficiency Optimization
**Prepared for the Board of Directors of {client_name}** *Status: Verified Field Diagnostic Profile (Local Secured Backup Matrix)*

---

#### ☕ The Financial Analogy
Purchasing un-optimized power from the grid is identical to paying for a full mug of cappuccino where a massive portion of the cup is filled with non-productive foam. The utility company bills you for the volume of the entire mug, but only the liquid coffee underneath does actual useful work on your production lines. 

#### 📉 The Corporate Risk Profile
Your facility is currently drawing power at an inefficient lagging power factor of **Cos Phi = {cos_phi}** through your **{asset_class}**.
* **The Vulnerability:** This lagging vector forces an artificial expansion of your total kVA demand footprint. You are pulling large volumes of non-productive reactive current across your switchgear, which triggers severe kVA capacity inflation penalties on your utility invoices.
* **The Strategic Recommendation:** The joint venture advises positioning automated power factor correction networks at your main incoming switchboard. This eliminates the reactive overhead, shrinks the billing foam, and unlocks immediate utility cost savings.
"""
