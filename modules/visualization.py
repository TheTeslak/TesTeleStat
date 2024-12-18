import matplotlib.pyplot as plt

def generate_personal_chat_plots(analysis_results, plot_filename_template, config, current_texts):
    if 'daily_user_messages' not in analysis_results:
        return

    daily_user_messages = analysis_results['daily_user_messages']
    daily_user_non_consecutive_messages = analysis_results['daily_user_non_consecutive_messages']
    daily_first_sender = analysis_results['daily_first_sender']

    all_dates = sorted(daily_user_messages.keys())
    if not all_dates:
        return

    years = sorted(set(date.year for date in all_dates))
    participants = list(analysis_results['user_counts'].keys())
    if len(participants) != 2:
        return
    user1, user2 = participants
    chat_name = analysis_results.get('chat_name', current_texts.get('no_name','Chat'))
    use_non_consecutive = config.get('plot_non_consecutive_messages', False)
    plot_data = daily_user_non_consecutive_messages if use_non_consecutive else daily_user_messages

    for year in years:
        dates = [date for date in all_dates if date.year == year]
        if not dates:
            continue
        user1_counts = [plot_data[date].get(user1, 0) for date in dates]
        user2_counts = [plot_data[date].get(user2, 0) for date in dates]

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(dates, user1_counts, label=user1, linewidth=2, alpha=0.7)
        ax.plot(dates, user2_counts, label=user2, linewidth=2, alpha=0.7)

        combined = user1_counts + user2_counts
        max_count = max(combined) if combined else 1
        triangle_y = max_count * 1.05
        first_sender_dates = [d for d in dates if d in daily_first_sender]
        sender_colors = ['blue' if daily_first_sender[d] == user1 else 'orange' for d in first_sender_dates]
        ax.scatter(first_sender_dates, [triangle_y]*len(first_sender_dates), color=sender_colors, marker='^', s=50, zorder=5)

        ax.set_xlabel(current_texts['date_label'])
        ax.set_ylabel(current_texts['message_count_label'])
        ax.set_title(current_texts['chat_activity_in_year'].format(year))

        triangle_label = current_texts.get('first_sender_triangle_label', 'First Sender After Interval')
        ax.scatter([], [], color='grey', marker='^', label=triangle_label)

        ax.legend()
        fig.autofmt_xdate()
        fig.tight_layout()
        plot_filename = plot_filename_template.replace('<year>', str(year))
        plt.savefig(plot_filename)
        plt.close()

def generate_group_chat_plots(analysis_results, plot_filename_template, config, current_texts):
    date_messages = analysis_results.get('date_messages', {})
    all_dates = sorted(date_messages.keys())
    if not all_dates:
        return

    years = sorted(set(date.year for date in all_dates))
    all_daily_counts = [date_messages[date] for date in all_dates]
    max_daily_messages = max(all_daily_counts) if all_daily_counts else 1

    for year in years:
        dates = [d for d in all_dates if d.year == year]
        if not dates:
            continue
        daily_counts = [date_messages[d] for d in dates]

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(dates, daily_counts, linewidth=2, alpha=0.7)
        ax.set_ylim(0, max_daily_messages * 1.1)

        ax.set_xlabel(current_texts['date_label'])
        ax.set_ylabel(current_texts['message_count_label'])
        ax.set_title(current_texts['group_chat_activity_in_year'].format(year))

        fig.autofmt_xdate()
        fig.tight_layout()
        plot_filename = plot_filename_template.replace('<year>', str(year))
        plt.savefig(plot_filename)
        plt.close()

def generate_channel_plots(analysis_results, plot_filename_template, config, current_texts):
    date_messages = analysis_results.get('date_messages', {})
    reactions_by_date = analysis_results.get('reactions_by_date', {})
    all_dates = sorted(set(date_messages.keys()) | set(reactions_by_date.keys()))
    if not all_dates:
        return

    years = sorted(set(d.year for d in all_dates))

    for year in years:
        dates = [d for d in all_dates if d.year == year]
        if not dates:
            continue
        daily_posts = [date_messages.get(d, 0) for d in dates]
        daily_reactions = [reactions_by_date.get(d, 0) for d in dates]

        fig, ax1 = plt.subplots(figsize=(12,6))
        ax1.plot(dates, daily_posts, color='tab:blue', linewidth=2, alpha=0.7, label=current_texts.get('posts_count_label','Posts'))
        ax1.set_xlabel(current_texts['date_label'])
        ax1.set_ylabel(current_texts['message_count_label'], color='tab:blue')
        ax1.tick_params(axis='y', labelcolor='tab:blue')

        ax2 = ax1.twinx()
        ax2.plot(dates, daily_reactions, color='tab:orange', linewidth=2, alpha=0.7, label=current_texts.get('reactions_count_label','Reactions'))
        ax2.set_ylabel(current_texts['reactions_count_label'], color='tab:orange')
        ax2.tick_params(axis='y', labelcolor='tab:orange')

        ax1.set_title(current_texts['channel_activity_in_year'].format(year))

        fig.autofmt_xdate()
        fig.tight_layout()
        plot_filename = plot_filename_template.replace('<year>', str(year))
        plt.savefig(plot_filename)
        plt.close()