"""
Rule Denied - League Notification
===================================
Sent to all league members when a rule proposal is denied.
Includes vote breakdown showing who voted yes/no.
"""

from lambdas.common.email_templates.base import (
    wrap_email_html,
    generate_section_title,
    generate_league_badge,
    generate_stamp,
    generate_vote_breakdown,
    generate_button,
    _escape,
    ERROR_RED, ACCENT_RED, TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED,
    DARK_NAVY, SURFACE_LIGHT,
    FONT_BODY, FONT_DISPLAY, XOMPER_URL,
)


def generate_rule_denied_email(
    proposer_name: str,
    rule_title: str,
    rule_description: str,
    approved_voters: list,
    rejected_voters: list,
    league_url: str = None,
    league_name: str = "",
) -> str:
    """Generate HTML email for denied rule notification."""
    url = league_url or XOMPER_URL
    safe_proposer = _escape(proposer_name)
    safe_title = _escape(rule_title)
    safe_desc = _escape(rule_description)
    yes_count = len(approved_voters)
    no_count = len(rejected_voters)

    content = f"""
    {generate_section_title("Rule Change Denied", ERROR_RED)}
    {generate_league_badge(league_name) if league_name else ""}

    <!-- DENIED stamp -->
    {generate_stamp("DENIED", ERROR_RED)}

    <!-- Rule title -->
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
            <td style="padding: 0 24px 6px; font-family: {FONT_BODY}; font-size: 20px;
                        font-weight: 700; color: {TEXT_MUTED}; line-height: 1.3;
                        text-decoration: line-through;">
                {safe_title}
            </td>
        </tr>
        <tr>
            <td style="padding: 0 24px 16px;">
                <span style="display: inline-block; padding: 4px 12px; background-color: {SURFACE_LIGHT};
                             border-radius: 20px; font-family: {FONT_BODY}; font-size: 12px;
                             font-weight: 600; color: {TEXT_SECONDARY};">
                    Proposed by {safe_proposer}
                </span>
            </td>
        </tr>
    </table>

    <!-- Rule description -->
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
            <td style="padding: 0 24px 20px;">
                <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"
                       style="background-color: {DARK_NAVY}; border: 1px solid {SURFACE_LIGHT};
                              border-radius: 10px; border-left: 4px solid {ERROR_RED};">
                    <tr>
                        <td style="padding: 16px 20px; font-family: {FONT_BODY}; font-size: 14px;
                                    color: {TEXT_MUTED}; line-height: 1.7;">
                            {safe_desc if safe_desc else '<em>No description provided.</em>'}
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>

    <!-- Result summary -->
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
            <td style="padding: 0 24px 8px; font-family: {FONT_BODY}; font-size: 14px;
                        color: {TEXT_PRIMARY}; text-align: center;">
                This rule has been <strong style="color: {ERROR_RED};">denied</strong>
                with {no_count} vote{"s" if no_count != 1 else ""} against
                and {yes_count} in favor. The required 2/3 majority was not reached.
            </td>
        </tr>
    </table>

    <!-- Vote breakdown -->
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
            <td style="padding: 8px 24px 4px; font-family: {FONT_BODY}; font-size: 12px; font-weight: 600;
                        text-transform: uppercase; letter-spacing: 0.05em; color: {TEXT_SECONDARY};">
                Vote Breakdown
            </td>
        </tr>
        <tr>
            <td style="padding: 0 24px 20px;">
                {generate_vote_breakdown(approved_voters, rejected_voters)}
            </td>
        </tr>
    </table>

    <!-- CTA -->
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
            <td style="padding: 0 24px 8px;" align="center">
                {generate_button("View League Rules", url)}
            </td>
        </tr>
    </table>
    """

    return wrap_email_html(
        content,
        preheader_text=f"Rule DENIED in {league_name}: {rule_title} ({yes_count}-{no_count} vote)" if league_name else f"Rule DENIED: {rule_title} ({yes_count}-{no_count} vote)"
    )


def generate_rule_denied_email_plain_text(
    proposer_name: str,
    rule_title: str,
    rule_description: str,
    approved_voters: list,
    rejected_voters: list,
    league_url: str = None,
    league_name: str = "",
) -> str:
    """Generate plain text version."""
    url = league_url or XOMPER_URL
    yes_count = len(approved_voters)
    no_count = len(rejected_voters)

    yes_names = ", ".join(approved_voters) if approved_voters else "None"
    no_names = ", ".join(rejected_voters) if rejected_voters else "None"
    league_line = f"League: {league_name}\n" if league_name else ""

    return (
        f"RULE DENIED\n"
        f"===========\n\n"
        f"{league_line}"
        f"Title: {rule_title}\n"
        f"Proposed by: {proposer_name}\n\n"
        f"Description:\n"
        f"{rule_description or 'No description provided.'}\n\n"
        f"Result: {yes_count} YES, {no_count} NO\n"
        f"The required 2/3 majority was not reached.\n\n"
        f"Voted Yes: {yes_names}\n"
        f"Voted No:  {no_names}\n\n"
        f"View league rules: {url}\n\n"
        f"---\n"
        f"Xomper Fantasy Football | xomper.com"
    )
