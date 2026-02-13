"""
Taxi Squad Steal - Target Owner Notification
=============================================
Sent to the owner whose taxi squad player is being stolen.
Includes compensation table and action instructions.
"""

from lambdas.common.email_templates.base import (
    wrap_email_html,
    generate_section_title,
    generate_league_badge,
    generate_player_card,
    generate_button,
    _escape,
    ACCENT_RED, CHAMPION_GOLD, TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED,
    DARK_NAVY, SURFACE_LIGHT, ERROR_RED, SUCCESS_GREEN,
    FONT_BODY, FONT_DISPLAY, FONT_MONO, XOMPER_URL,
)

# Default taxi steal compensation per league rules
DEFAULT_COMPENSATION = [
    {"round_taken": "1st Round", "cost": "1st + 2nd Round Pick"},
    {"round_taken": "2nd Round", "cost": "1st Round Pick"},
    {"round_taken": "3rd Round", "cost": "2nd Round Pick"},
    {"round_taken": "4th Round", "cost": "3rd Round Pick"},
    {"round_taken": "5th Round", "cost": "4th Round Pick"},
    {"round_taken": "Undrafted", "cost": "5th Round Pick"},
]


def generate_taxi_steal_owner_email(
    stealer_name: str,
    player_name: str,
    player_position: str,
    player_team: str,
    owner_name: str,
    compensation_table: list = None,
    league_url: str = None,
    league_name: str = "",
) -> str:
    """Generate HTML email for taxi squad steal target owner notification."""
    url = league_url or XOMPER_URL
    safe_stealer = _escape(stealer_name)
    safe_player = _escape(player_name)
    safe_owner = _escape(owner_name)
    comp_table = compensation_table or DEFAULT_COMPENSATION

    # Build compensation rows
    comp_rows = ""
    for row in comp_table:
        comp_rows += f"""
        <tr>
            <td style="padding: 8px 12px; font-family: {FONT_BODY}; font-size: 13px;
                        color: {TEXT_PRIMARY}; border-bottom: 1px solid {SURFACE_LIGHT};">
                {_escape(row.get('round_taken', ''))}
            </td>
            <td style="padding: 8px 12px; font-family: {FONT_MONO}; font-size: 13px;
                        color: {CHAMPION_GOLD}; border-bottom: 1px solid {SURFACE_LIGHT};">
                {_escape(row.get('cost', ''))}
            </td>
        </tr>
        """

    content = f"""
    {generate_section_title("Your Taxi Squad Is Under Attack", ACCENT_RED)}
    {generate_league_badge(league_name) if league_name else ""}

    <!-- Main message -->
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
            <td style="padding: 0 24px 16px; font-family: {FONT_BODY}; font-size: 16px; line-height: 1.6; color: {TEXT_PRIMARY};">
                <strong style="color: {ACCENT_RED};">{safe_stealer}</strong> is trying to steal
                <strong>{safe_player}</strong> from your taxi squad!
            </td>
        </tr>
    </table>

    <!-- Player card -->
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
            <td style="padding: 0 24px 20px;">
                {generate_player_card(player_name, player_position, player_team)}
            </td>
        </tr>
    </table>

    <!-- Action required banner -->
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
            <td style="padding: 0 24px 16px;">
                <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"
                       style="background-color: rgba(255,71,87,0.08); border: 1px solid {ACCENT_RED};
                              border-radius: 10px; border-left: 4px solid {ACCENT_RED};">
                    <tr>
                        <td style="padding: 16px 20px;">
                            <div style="font-family: {FONT_DISPLAY}; font-size: 18px; letter-spacing: 0.05em;
                                        color: {ACCENT_RED}; margin-bottom: 8px;">
                                ACTION REQUIRED
                            </div>
                            <div style="font-family: {FONT_BODY}; font-size: 14px; color: {TEXT_PRIMARY}; line-height: 1.6;">
                                You have until <strong>Thursday 12:00 PM EST</strong> to respond. You have two options:
                            </div>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>

    <!-- Option 1 -->
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
            <td style="padding: 0 24px 12px;">
                <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"
                       style="background-color: {DARK_NAVY}; border: 1px solid {SURFACE_LIGHT};
                              border-radius: 10px; border-left: 4px solid {SUCCESS_GREEN};">
                    <tr>
                        <td style="padding: 14px 18px;">
                            <div style="font-family: {FONT_BODY}; font-size: 14px; font-weight: 700;
                                        color: {SUCCESS_GREEN}; margin-bottom: 4px;">
                                Option 1: Promote to Active Roster
                            </div>
                            <div style="font-family: {FONT_BODY}; font-size: 13px; color: {TEXT_SECONDARY}; line-height: 1.5;">
                                Elevate {safe_player} from your taxi squad to your active roster before the deadline.
                                This nullifies the steal attempt and you keep the player.
                            </div>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>

    <!-- Option 2 -->
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
            <td style="padding: 0 24px 20px;">
                <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"
                       style="background-color: {DARK_NAVY}; border: 1px solid {SURFACE_LIGHT};
                              border-radius: 10px; border-left: 4px solid {CHAMPION_GOLD};">
                    <tr>
                        <td style="padding: 14px 18px;">
                            <div style="font-family: {FONT_BODY}; font-size: 14px; font-weight: 700;
                                        color: {CHAMPION_GOLD}; margin-bottom: 4px;">
                                Option 2: Accept Draft Pick Compensation
                            </div>
                            <div style="font-family: {FONT_BODY}; font-size: 13px; color: {TEXT_SECONDARY}; line-height: 1.5;">
                                Let the steal go through. {safe_stealer} takes {safe_player} and you receive
                                draft pick compensation based on the round the player was originally drafted.
                            </div>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>

    <!-- Compensation table -->
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
            <td style="padding: 0 24px 4px; font-family: {FONT_BODY}; font-size: 12px; font-weight: 600;
                        text-transform: uppercase; letter-spacing: 0.05em; color: {TEXT_SECONDARY};">
                Taxi Steal Compensation
            </td>
        </tr>
        <tr>
            <td style="padding: 0 24px 20px;">
                <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"
                       style="background-color: {DARK_NAVY}; border: 1px solid {SURFACE_LIGHT}; border-radius: 10px; overflow: hidden;">
                    <tr style="background-color: {SURFACE_LIGHT};">
                        <td style="padding: 8px 12px; font-family: {FONT_BODY}; font-size: 12px;
                                    font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;
                                    color: {CHAMPION_GOLD};">
                            Round Taken
                        </td>
                        <td style="padding: 8px 12px; font-family: {FONT_BODY}; font-size: 12px;
                                    font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;
                                    color: {CHAMPION_GOLD};">
                            Minimum Cost
                        </td>
                    </tr>
                    {comp_rows}
                </table>
            </td>
        </tr>
    </table>

    <!-- CTA -->
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
            <td style="padding: 4px 24px 8px;" align="center">
                {generate_button("Take Action Now", url, ACCENT_RED, "#ffffff")}
            </td>
        </tr>
    </table>
    """

    return wrap_email_html(
        content,
        preheader_text=f"URGENT: {stealer_name} is trying to steal {player_name} from your taxi squad! Take action before Thursday."
    )


def generate_taxi_steal_owner_email_plain_text(
    stealer_name: str,
    player_name: str,
    player_position: str,
    player_team: str,
    owner_name: str,
    compensation_table: list = None,
    league_url: str = None,
    league_name: str = "",
) -> str:
    """Generate plain text version."""
    url = league_url or XOMPER_URL
    comp_table = compensation_table or DEFAULT_COMPENSATION

    comp_lines = "\n".join(
        f"  {row.get('round_taken', '')}: {row.get('cost', '')}"
        for row in comp_table
    )

    league_line = f"League: {league_name}\n" if league_name else ""
    return (
        f"YOUR TAXI SQUAD IS UNDER ATTACK\n"
        f"================================\n\n"
        f"{league_line}"
        f"{stealer_name} is trying to steal {player_position} {player_name} ({player_team}) "
        f"from your taxi squad!\n\n"
        f"ACTION REQUIRED - You have until Thursday 12:00 PM EST to respond.\n\n"
        f"Option 1: Promote to Active Roster\n"
        f"  Elevate {player_name} to your active roster before the deadline.\n"
        f"  This nullifies the steal attempt.\n\n"
        f"Option 2: Accept Draft Pick Compensation\n"
        f"  Let the steal go through and receive picks based on when the player was drafted.\n\n"
        f"Compensation Table:\n"
        f"{comp_lines}\n\n"
        f"Take action: {url}\n\n"
        f"---\n"
        f"Xomper Fantasy Football | xomper.com"
    )
