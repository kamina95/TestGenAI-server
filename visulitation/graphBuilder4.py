import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def load_and_process_data(filepath):
    # Load the data from a CSV file
    data = pd.read_csv(filepath)
    print(f"Total rows loaded: {len(data)}")

    # Remove extreme outliers if necessary
    data = data[data['LineCount'] < 1000]
    print(f"Rows retained for analysis: {len(data)}")

    # Select only numeric columns for averaging
    numeric_cols = data.select_dtypes(include=['number']).columns.tolist()
    numeric_cols.remove('LineCount')  # Avoid duplicating 'LineCount' in the join

    # Average the metrics for duplicate class names using only numeric columns
    averaged_data = data.groupby('ClassName')[numeric_cols].mean().reset_index()

    # Re-include class names and Line Count for plotting
    class_data = data[['ClassName', 'LineCount']].drop_duplicates().set_index('ClassName')
    averaged_data = averaged_data.set_index('ClassName').join(class_data)

    return averaged_data.reset_index()

def plot_coverage_improvements(data):
    # Sorting data for better visualization
    data = data.sort_values(by='LineCount')

    # Define the number of classes and their positions
    n_classes = len(data)
    index = np.arange(n_classes)
    bar_width = 0.35

    # Create subplots to plot branch and instruction coverage improvements
    fig, ax = plt.subplots(2, 1, figsize=(14, 12))

    # Plotting Branch Coverage Improvement
    ax[0].bar(index, data['BRANCH-I-C'], bar_width, label='Initial Branch Coverage', color='b')
    ax[0].bar(index + bar_width, data['BRANCH-G-C'], bar_width, label='Final Branch Coverage', color='g')

    # Plotting Instruction Coverage Improvement
    ax[1].bar(index, data['INSTRUCTION-I-C'], bar_width, label='Initial Instruction Coverage', color='r')
    ax[1].bar(index + bar_width, data['INSTRUCTION-G-C'], bar_width, label='Final Instruction Coverage', color='y')

    # Add labels, title, and legend with class name and number of lines in the x-axis labels
    labels = [f"{name} ({int(lines)} lines)" for name, lines in zip(data['ClassName'], data['LineCount'])]

    ax[0].set_xlabel('Class Name with Number of Lines')
    ax[0].set_ylabel('Coverage %')
    ax[0].set_title('Branch Coverage Improvement')
    ax[0].set_xticks(index + bar_width / 2)
    ax[0].set_xticklabels(labels, rotation=45)
    ax[0].legend()

    ax[1].set_xlabel('Class Name with Number of Lines')
    ax[1].set_ylabel('Coverage %')
    ax[1].set_title('Instruction Coverage Improvement')
    ax[1].set_xticks(index + bar_width / 2)
    ax[1].set_xticklabels(labels, rotation=45)
    ax[1].legend()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    filepath = 'C:\\Users\\Antonio\\Downloads\\apiTester\\coveragePercentages.csv'  # Modify this line to the path of your CSV file
    processed_data = load_and_process_data(filepath)
    plot_coverage_improvements(processed_data)
