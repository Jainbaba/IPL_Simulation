import random


class Feild:
    """
    Feild class to handle field conditions for a cricket match simulation.

    Methods:

    get_field_status():
      - Prompts user input for dew, pitch deterioration, pitch type
      - Returns:
        - dew (bool): Whether dew is present
        - pitch_deterioration (bool): Whether pitch is expected to deteriorate
        - pitch_type (str): "dusty", "green", or "dead"

    pitch_info():
      - Generates pace and spin factors based on pitch type
      - Parameters:
        - pitch_type (str): "dusty", "green", or "dead"
      - Returns:
        - pace (float): Pace bowling pitch factor
        - spin (float): Spin bowling pitch factor"""

    def get_field_status(self):
        while True:
            dew_choice = input(
                "Is there dew on the field? (Enter 'yes' or 'no', leave blank for default): "
            )
            pitch_deterioration_choice = input(
                "Is the pitch expected to deteriorate? (Enter 'yes' or 'no', leave blank for default): "
            )
            pitch_type_choice = input(
                "What is the type of pitch? (Enter 'Dusty', 'Green', or 'Dead', leave blank for default): "
            )

            if dew_choice.lower() == "yes":
                dew = True
            elif dew_choice.lower() == "no":
                dew = False
            elif dew_choice == "":
                dew = True  # Default value
            else:
                print("Invalid input. Please enter 'yes' or 'no' for dew status.")
                continue

            if pitch_deterioration_choice.lower() == "yes":
                pitch_deterioration = True
            elif pitch_deterioration_choice.lower() == "no":
                pitch_deterioration = False
            elif pitch_deterioration_choice == "":
                pitch_deterioration = False  # Default value
            else:
                print(
                    "Invalid input. Please enter 'yes' or 'no' for pitch deterioration status."
                )
                continue

            if pitch_type_choice.lower() in ["dusty", "green", "dead"]:
                pitch_type = pitch_type_choice.lower()
            elif pitch_type_choice == "":
                pitch_type = "dusty"  # Default value
            else:
                print(
                    "Invalid input. Please enter 'Dusty', 'Green', or 'Dead' for pitch type."
                )
                continue

            break
        print(f"\nField Status:")
        print(f"Dew: {dew}")
        print(f"Pitch Deterioration: {pitch_deterioration}")
        print(f"Pitch Type: {pitch_type.capitalize()}")
        print(
            "--------------------------------------------------------------------------"
        )
        return dew, pitch_deterioration, pitch_type

    def pitch_info(self, pitch_type):
        if pitch_type == "dusty":
            pace = 1 + 0.5 * (random.random() * 0.0)
            spin = 1 + 0.5 * (random.random() * 0.0)
            spin = spin - random.uniform(0.1, 0.16)
        elif pitch_type == "green":
            pace = 1 + 0.5 * (random.random() * 0.0)
            pace = pace - random.uniform(0.1, 0.16)
            spin = 1 + 0.5 * (random.random() * 0.0)
        elif pitch_type == "dead":
            pace = 1 + 0.5 * (random.random() * 0.0)
            spin = 1 + 0.5 * (random.random() * 0.0)
        return pace, spin
