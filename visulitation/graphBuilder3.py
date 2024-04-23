import pandas as pd
import matplotlib.pyplot as plt


def load_and_process_data(filepath):
    # Load the data from a CSV file
    data = pd.read_csv(filepath)

    print(f"Total rows loaded: {len(data)}")

    # Remove extreme outliers if necessary (adjust or remove this line if not needed)
    data = data[data['LineCount'] < 1000]

    # Keep all rows, not just those with improvements
    print(f"Rows retained for analysis: {len(data)}")

    # Select only numeric columns for averaging
    numeric_cols = data.select_dtypes(include=['number']).columns.tolist()
    numeric_cols.remove('LineCount')  # Ensure 'LineCount' is not duplicated in the join

    # Average the metrics for duplicate class names, using only numeric columns
    averaged_data = data.groupby('ClassName')[numeric_cols].mean().reset_index()

    # Re-include class names and Line Count for plotting
    class_data = data[['ClassName', 'LineCount']].drop_duplicates().set_index('ClassName')
    averaged_data = averaged_data.set_index('ClassName').join(class_data)

    return averaged_data.reset_index()


def plot_line_coverage_vs_lines(data):
    plt.figure(figsize=(10, 8))

    # Sorting data for meaningful line connections
    data = data.sort_values(by='LineCount')

    # Plotting Initial and Final Line Coverage as lines
    plt.plot(data['LineCount'], data['LINE-I-C'], marker='o', linestyle='-', color='blue',
             label='Initial Line Coverage')
    plt.plot(data['LineCount'], data['LINE-G-C'], marker='o', linestyle='--', color='green',
             label='Final Line Coverage')

    # Adding class names as labels next to each point
    for index, row in data.iterrows():
        plt.text(row['LineCount'], row['LINE-I-C'], row['ClassName'], fontsize=9, verticalalignment='bottom')
        plt.text(row['LineCount'], row['LINE-G-C'], row['ClassName'], fontsize=9, verticalalignment='top')

    plt.title('Line Coverage Before and After vs. Number of Lines')
    plt.xlabel('Number of Lines')
    plt.ylabel('Line Coverage (%)')
    plt.legend()

    # Optionally turn off the grid
    plt.grid(False)

    plt.show()


if __name__ == "__main__":
    filepath = 'C:\\Users\\Antonio\\Downloads\\apiTester\\coveragePercentages.csv'  # Modify this line to the path of your CSV file
    processed_data = load_and_process_data(filepath)
    plot_line_coverage_vs_lines(processed_data)
