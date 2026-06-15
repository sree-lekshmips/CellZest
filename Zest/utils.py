import matplotlib.pyplot as plt
import base64
from io import BytesIO

def create_anemia_graph(gender, hemoglobin_level, severity):
    # Define the severity thresholds for male and female
    thresholds = {
        'Male': {
            'Normal': (15, float('inf')),
            'Mild': (13, 15),
            'Moderate': (12, 13),
            'Severe': (6, 12)
        },
        'Female': {
            'Normal': (14, float('inf')),
            'Mild': (12, 14),
            'Moderate': (11, 12),
            'Severe': (6, 11)
        }
    }

    # Get the thresholds for the specified gender
    gender_thresholds = thresholds[gender]

    # Create a bar graph
    categories = list(gender_thresholds.keys())
    values = [threshold[0] for threshold in gender_thresholds.values()]
    color_map = {
        'Normal': 'green',
        'Mild': 'blue',
        'Moderate': 'orange',
        'Severe': 'red'
    }

    # Highlight the user's hemoglobin level
    user_value = hemoglobin_level
    colors = ['#D8BFD8' if category != severity else color_map[category] for category in categories]




    plt.figure(figsize=(8, 5), facecolor=(1, 1, 1, 0.0))
    plt.bar(categories, values, color=colors, alpha=0.6)
    plt.axhline(y=user_value, color='blue', linestyle='--', label='Your Hemoglobin Level')
    plt.title(f'Anemia Severity Based on Hemoglobin Level for {gender}')
    plt.ylabel('Hemoglobin Level')
    plt.xlabel('Severity Categories')
    plt.legend()

    # Save the plot to a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Encode the image to base64
    graph = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return graph