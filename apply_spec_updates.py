import os
import re


def refactor_codebase(target_directory="src"):
    """
    Scans all Python files inside the target directory and converts
    deprecated 'use_container_width' parameters to the updated 'width' specification.
    """
    # Regex patterns to handle varied spacing around assignment operators
    true_pattern = re.compile(r"use_container_width\s*=\s*True")
    false_pattern = re.compile(r"use_container_width\s*=\s*False")

    modified_files_count = 0
    total_substitutions = 0

    print(
        f"🚀 Initialising STEM Codebase Refactoring Sweep inside: /{target_directory}"
    )
    print("-" * 70)

    for root, _, files in os.walk(target_directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)

                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Calculate substitutions required in this specific file
                file_subs = len(true_pattern.findall(content)) + len(
                    false_pattern.findall(content)
                )

                if file_subs > 0:
                    # Execute replacements inline
                    updated_content = true_pattern.sub('width="stretch"', content)
                    updated_content = false_pattern.sub(
                        'width="content"', updated_content
                    )

                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(updated_content)

                    print(f"✅ Refactored: {file_path} -> Applied {file_subs} fixes.")
                    modified_files_count += 1
                    total_substitutions += file_subs

    print("-" * 70)
    print(
        f"🏁 Sweep Complete. Modified {modified_files_count} files with {total_substitutions} total updates applied."
    )


if __name__ == "__main__":
    # Execute refactoring against your source folder node
    refactor_codebase("src")
