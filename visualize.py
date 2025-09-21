import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def plot_avg_hourly_bar_chart(csv_path='summaries/hourly_summary.csv'):
    df = pd.read_csv(csv_path)

    # Extract hour of the day
    df['HourOfDay'] = df['Hour'].str[11:13]

    # Group by hour and calculate average
    hourly_avg = df.groupby('HourOfDay')['Messages'].mean().reset_index()

    # Sort hours in correct order
    hourly_avg = hourly_avg.sort_values('HourOfDay')

    # Plot
    plt.figure(figsize=(12, 6))
    bars = plt.bar(hourly_avg['HourOfDay'], hourly_avg['Messages'], color='mediumseagreen')

    plt.title('Average Messages per Hour of Day')
    plt.xlabel('Hour (24h)')
    plt.ylabel('Average Message Count')

    # Use integer ticks on y-axis
    plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    # Annotate each bar with its value
    for bar in bars:
        height = bar.get_height()
        plt.annotate(f'{height:.1f}',
                     xy=(bar.get_x() + bar.get_width() / 2, height),
                     xytext=(0, 3),  # 3 points vertical offset
                     textcoords="offset points",
                     ha='center', va='bottom', fontsize=9)

    plt.tight_layout()
    plt.savefig('summaries/hourly_avg_bar_annotated.png')
    plt.show()


def plot_total_messages_half_yearly(csv_path='summaries/hourly_summary.csv'):
    df = pd.read_csv(csv_path)

    # Convert Hour column to datetime
    df['Hour'] = pd.to_datetime(df['Hour'])

    # Calculate half-year as a float: year + 0 for H1, + 0.5 for H2
    df['HalfYear'] = df['Hour'].dt.year + ((df['Hour'].dt.month - 1) // 6) * 0.5

    # Group by half-year and sum messages
    half_yearly_total = df.groupby('HalfYear')['Messages'].sum().reset_index()

    plt.figure(figsize=(10, 6))
    plt.bar(half_yearly_total['HalfYear'], half_yearly_total['Messages'], color='purple', width=0.4)

    plt.title('Total Messages per Half-Yearly')
    plt.xlabel('Year')
    plt.ylabel('Total Messages')

    plt.xticks(half_yearly_total['HalfYear'], rotation=45)

    plt.tight_layout()
    plt.savefig('summaries/half_yearly_total_messages.png')
    plt.show()


if __name__ == "__main__":
    plot_avg_hourly_bar_chart()
    plot_total_messages_half_yearly()
