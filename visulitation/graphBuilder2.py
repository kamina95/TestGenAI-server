import pandas as pd
import matplotlib.pyplot as plt


def load_and_process_data(filepath):
    # Load the data from a CSV file
    data = pd.read_csv(filepath)

    print(f"Total rows loaded: {len(data)}")

    # Optionally, remove any extreme outliers if necessary (like very large classes)
    data = data[data['LineCount'] < 1000]  # Adjust this if needed

    # Remove rows where there is no improvement
    filtered_data = data[(data["BRANCH-Diff"] > 0) | (data["INSTRUCTION-Diff"] > 0) | (data["LINE-Diff"] > 0)]
    print(f"Rows after filtering for improvements: {len(filtered_data)}")

    # Select only numeric columns for averaging (excluding 'LineCount' and 'LLM')
    numeric_cols = filtered_data.select_dtypes(include=['number']).columns.tolist()

    # Average the metrics for duplicate class names, using only numeric columns
    averaged_data = filtered_data.groupby('ClassName')[numeric_cols].mean().reset_index()

    return averaged_data


def analyze_line_count(data):
    # Analyze LineCount distribution
    print("LineCount Distribution:")
    print(data['LineCount'].describe())

    # Visualize the distribution
    plt.figure()
    plt.hist(data['LineCount'], bins=30, color='blue', alpha=0.7)
    plt.title('Line Count Distribution')
    plt.xlabel('Line Count')
    plt.ylabel('Frequency')
    plt.show()


def categorize_and_plot(data):
    # Determine suitable thresholds based on the distribution
    small_threshold = 50  # Update these based on your histogram observation
    medium_threshold = 200  # Update these based on your histogram observation

    # Categorize based on LineCount
    data['SizeCategory'] = pd.cut(data['LineCount'], bins=[0, small_threshold, medium_threshold, float('inf')],
                                  labels=['Small', 'Medium', 'Large'])
    print(data['SizeCategory'].value_counts())  # Print the counts of each category

    # Plotting
    for category in ['Small', 'Medium', 'Large']:
        subset = data[data['SizeCategory'] == category]
        if subset.empty:
            print(f"No data available for {category} classes to plot.")
            continue

        plt.figure()
        plt.title(f'Line Coverage Improvement for {category} Classes')
        plt.plot(subset['ClassName'], subset['LINE-I-C'], marker='o', linestyle='-', label='Initial Line Coverage')
        plt.plot(subset['ClassName'], subset['LINE-G-C'], marker='o', linestyle='--', label='Final Line Coverage')
        plt.xticks(rotation=45)
        plt.ylabel('Line Coverage (%)')
        plt.xlabel('Class Name')
        plt.legend()
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    filepath = 'C:\\Users\\Antonio\\Downloads\\apiTester\\coveragePercentages.csv'  # Modify this line to the path of your CSV file
    processed_data = load_and_process_data(filepath)
    analyze_line_count(processed_data)
    categorize_and_plot(processed_data)
