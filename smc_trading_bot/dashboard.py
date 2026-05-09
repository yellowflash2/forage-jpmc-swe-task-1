def render(stats: dict) -> str:
    return (
        f"Mode: {stats['mode']}\n"
        f"Setups: {stats['setups']}\n"
        f"Trades: {stats['trades']}\n"
        f"Daily R: {stats['daily_r']:.2f}\n"
        f"Weekly R: {stats['weekly_r']:.2f}\n"
    )
