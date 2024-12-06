import matplotlib.pyplot as plt

def generate_personal_chat_plots(analysis_results, plot_filename_template, config, current_texts):
    # Generates line plots showing how two participants' activity changes over time.
    # If plot_non_consecutive_messages = True, shows non-consecutive counts instead of total daily counts.
    daily_user_messages = analysis_results['daily_user_messages']
    daily_user_non_consecutive_messages = analysis_results['daily_user_non_consecutive_messages']
    daily_first_sender = analysis_results['daily_first_sender']

    all_dates = sorted(daily_user_messages.keys())
    years = sorted(set(date.year for date in all_dates))

    participants = list(analysis_results['user_counts'].keys())
    if len(participants) != 2:
        # For personal charts we expect exactly 2 participants.
        return
    user1, user2 = participants

    chat_name = analysis_results.get('chat_name', 'Chat')

    if config.get('plot_non_consecutive_messages', False):
        plot_data = daily_user_non_consecutive_messages
    else:
        plot_data = daily_user_messages

    for year in years:
        dates = [date for date in all_dates if date.year == year]
        user1_counts = [plot_data[date].get(user1, 0) for date in dates]
        user2_counts = [plot_data[date].get(user2, 0) for date in dates]

        plt.figure(figsize=(12, 6))
        plt.plot(dates, user1_counts, label=user1, linewidth=2, alpha=0.7)
        plt.plot(dates, user2_counts, label=user2, linewidth=2, alpha=0.7)

        plt.ylim(bottom=0)

        # Marking with a triangle the first sender after a break each day at a level slightly above max counts.
        max_count = max(user1_counts + user2_counts) if (user1_counts + user2_counts) else 1
        triangle_y = max_count * 1.05
        first_sender_dates = [date for date in dates if date in daily_first_sender]
        sender_colors = ['blue' if daily_first_sender[date] == user1 else 'orange' for date in first_sender_dates]
        plt.scatter(first_sender_dates, [triangle_y]*len(first_sender_dates), color=sender_colors, marker='^', s=50, zorder=5)

        plt.xlabel(current_texts.get('date_label', 'Date'))
        plt.ylabel(current_texts.get('message_count_label', 'Number of Messages'))
        plt.title(f"{chat_name} - {current_texts.get('chat_activity_in_year', 'Chat Activity in {0}').format(year)}")

        # Add a legend marker for the first sender triangles.
        triangle_label = current_texts.get('first_sender_triangle_label', 'First Sender After Interval')
        plt.scatter([], [], color='grey', marker='^', label=triangle_label)

        plt.legend()
        plt.tight_layout()
        plot_filename = plot_filename_template.replace('<year>', str(year))
        plt.savefig(plot_filename)
        plt.close()

def generate_group_chat_plots(analysis_results, plot_filename_template, config, current_texts):
    # Generates a line plot of total messages per day for a group chat.
    date_messages = analysis_results['date_messages']

    all_dates = sorted(date_messages.keys())
    years = sorted(set(date.year for date in all_dates))

    all_daily_counts = [date_messages[date] for date in all_dates]
    max_daily_messages = max(all_daily_counts) if all_daily_counts else 1

    chat_name = analysis_results.get('chat_name', 'Chat')

    for year in years:
        dates = [date for date in all_dates if date.year == year]
        daily_counts = [date_messages[date] for date in dates]

        plt.figure(figsize=(12, 6))
        plt.plot(dates, daily_counts, linewidth=2, alpha=0.7)

        plt.ylim(0, max_daily_messages * 1.1)

        plt.xlabel(current_texts.get('date_label', 'Date'))
        plt.ylabel(current_texts.get('message_count_label', 'Number of Messages'))
        plt.title(f"{chat_name} - {current_texts.get('group_chat_activity_in_year', 'Group Chat Activity in {0}').format(year)}")

        plt.tight_layout()
        plot_filename = plot_filename_template.replace('<year>', str(year))
        plt.savefig(plot_filename)
        plt.close()