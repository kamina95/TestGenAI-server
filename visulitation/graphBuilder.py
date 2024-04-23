import pandas as pd
import matplotlib.pyplot as plt


def load_and_process_data(filepath):
    # Load the data from a CSV file
    data = pd.read_csv(filepath)

    # Remove rows where there is no improvement
    filtered_data = data[(data["BRANCH-Diff"] > 0) | (data["INSTRUCTION-Diff"] > 0) | (data["LINE-Diff"] > 0)]

    # Select only numeric columns for averaging (excluding 'LineCount' and 'LLM')
    numeric_cols = filtered_data.select_dtypes(include=['number']).columns.tolist()

    # Average the metrics for duplicate class names, using only numeric columns
    averaged_data = filtered_data.groupby('ClassName')[numeric_cols].mean().reset_index()

    return averaged_data


def categorize_and_plot(data):
    # Determine thresholds for class sizes
    small_threshold = 40
    medium_threshold = 70

    # Categorize based on LineCount
    data['SizeCategory'] = pd.cut(data['LineCount'], bins=[0, small_threshold, medium_threshold, float('inf')],
                                  labels=['Small', 'Medium', 'Large'])

    # Plotting
    for category in ['Small', 'Medium', 'Large']:
        subset = data[data['SizeCategory'] == category]
        plt.figure()
        plt.title(f'Line Coverage Improvement for {category} Classes')
        plt.plot(subset['ClassName'], subset['LINE-I-C'], label='Initial Line Coverage')
        plt.plot(subset['ClassName'], subset['LINE-G-C'], label='Final Line Coverage')
        plt.xticks(rotation=45)
        plt.ylabel('Line Coverage (%)')
        plt.xlabel('Class Name')
        plt.legend()
        plt.tight_layout()
        plt.show()




if __name__ == "__main__":
    filepath = 'C:\\Users\\Antonio\\Downloads\\apiTester\\coveragePercentages.csv'  # Modify this line to the path of your CSV file
    processed_data = load_and_process_data(filepath)
    categorize_and_plot(processed_data)
