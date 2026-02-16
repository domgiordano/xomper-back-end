"""
Taxi Squad Steal - League Notification
=======================================
Sent to all league members when someone initiates a taxi squad steal.
"""

from lambdas.common.email_templates.base import (
    wrap_email_html,
    generate_section_title,
    generate_league_badge,
    generate_player_card,
    generate_button,
    _escape,
    CHAMPION_GOLD, TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED, DARK_NAVY,
    SURFACE_LIGHT, FONT_BODY, FONT_DISPLAY, FONT_MONO, XOMPER_URL,
)


def generate_taxi_steal_league_email(
    stealer_name: str,
    player_name: str,
    player_position: str,
    player_team: str,
    target_owner_name: str,
    league_url: str = None,
    league_name: str = "",
    player_image_url: str = "",
    team_logo_url: str = "",
    pick_cost: str = "",
) -> str:
    """Generate HTML email for taxi squad steal league notification."""
    url = league_url or XOMPER_URL
    safe_stealer = _escape(stealer_name)
    safe_player = _escape(player_name)
    safe_owner = _escape(target_owner_name)
    safe_cost = _escape(pick_cost)

    # Pick cost badge
    cost_html = ""
    if pick_cost:
        cost_html = f"""
        <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
            <tr>
                <td style="padding: 0 24px 16px;">
                    <table role="presentation" cellpadding="0" cellspacing="0" border="0"
                           style="background-color: {DARK_NAVY}; border: 1px solid {SURFACE_LIGHT}; border-radius: 8px;">
                        <tr>
                            <td style="padding: 10px 16px;">
                                <span style="font-family: {FONT_BODY}; font-size: 12px; font-weight: 600;
                                             text-transform: uppercase; letter-spacing: 0.05em; color: {TEXT_SECONDARY};">
                                    Stealing for:
                                </span>
                                <span style="font-family: {FONT_MONO}; font-size: 15px; font-weight: 700;
                                             color: {CHAMPION_GOLD}; margin-left: 8px;">
                                    {safe_cost}
                                </span>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
        """

    content = f"""
    {generate_section_title("Taxi Squad Alert")}
    {generate_league_badge(league_name) if league_name else ""}

    <!-- Main message -->
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
            <td style="padding: 0 24px 16px; font-family: {FONT_BODY}; font-size: 16px; line-height: 1.6; color: {TEXT_PRIMARY};">
                <strong style="color: {CHAMPION_GOLD};">{safe_stealer}</strong> is trying to steal
                <strong>{safe_player}</strong> from
                <strong style="color: {CHAMPION_GOLD};">{safe_owner}</strong>&rsquo;s taxi squad!
            </td>
        </tr>
    </table>

    <!-- Player card -->
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
            <td style="padding: 0 24px 20px;">
                {generate_player_card(player_name, player_position, player_team, player_image_url, team_logo_url)}
            </td>
        </tr>
    </table>

    {cost_html}

    <!-- Explanation -->
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
            <td style="padding: 0 24px 8px; font-family: {FONT_BODY}; font-size: 13px; color: {TEXT_SECONDARY}; line-height: 1.6;">
                {safe_owner} has until <strong style="color: {TEXT_PRIMARY};">Thursday 12:00 PM EST</strong>
                to promote the player from their taxi squad. Otherwise, the steal goes through
                and {safe_stealer} receives the player in exchange for draft pick compensation.
            </td>
        </tr>
    </table>

    <!-- CTA -->
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
            <td style="padding: 20px 24px 8px;" align="center">
                {generate_button("View on Xomper", url)}
            </td>
        </tr>
    </table>
    """

    return wrap_email_html(
        content,
        preheader_text=f"{stealer_name} is trying to steal {player_name} from {target_owner_name}'s taxi squad!"
    )


def generate_taxi_steal_league_email_plain_text(
    stealer_name: str,
    player_name: str,
    player_position: str,
    player_team: str,
    target_owner_name: str,
    league_url: str = None,
    league_name: str = "",
    pick_cost: str = "",
    **kwargs,
) -> str:
    """Generate plain text version."""
    url = league_url or XOMPER_URL
    league_line = f"League: {league_name}\n" if league_name else ""
    cost_line = f"Stealing for: {pick_cost}\n\n" if pick_cost else ""
    return (
        f"TAXI SQUAD ALERT\n"
        f"================\n\n"
        f"{league_line}"
        f"{stealer_name} is trying to steal {player_position} {player_name} ({player_team}) "
        f"from {target_owner_name}'s taxi squad!\n\n"
        f"{cost_line}"
        f"{target_owner_name} has until Thursday 12:00 PM EST to promote the player "
        f"from their taxi squad. Otherwise, the steal goes through and {stealer_name} "
        f"receives the player in exchange for draft pick compensation.\n\n"
        f"View on Xomper: {url}\n\n"
        f"---\n"
        f"Xomper Fantasy Football | xomper.com"
    )
