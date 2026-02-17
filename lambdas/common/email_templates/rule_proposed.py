"""
Rule Proposed - League Notification
====================================
Sent to all league members when a new rule is proposed.
"""

from lambdas.common.email_templates.base import (
    wrap_email_html,
    generate_section_title,
    generate_league_badge,
    generate_button,
    _escape,
    CHAMPION_GOLD, TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED,
    DARK_NAVY, SURFACE_LIGHT,
    FONT_BODY, FONT_DISPLAY, FONT_MONO, XOMPER_URL,
)


def generate_rule_proposed_email(
    proposer_name: str,
    rule_title: str,
    rule_description: str,
    vote_url: str = None,
    league_name: str = "",
) -> str:
    """Generate HTML email for new rule proposal notification."""
    url = vote_url or XOMPER_URL
    safe_proposer = _escape(proposer_name)
    safe_title = _escape(rule_title)
    safe_desc = _escape(rule_description)

    content = f"""
    {generate_section_title("New Rule Proposal")}
    {generate_league_badge(league_name) if league_name else ""}

    <!-- Proposer badge -->
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
            <td style="padding: 0 24px 16px;">
                <span style="display: inline-block; padding: 4px 12px; background-color: {SURFACE_LIGHT};
                             border-radius: 20px; font-family: {FONT_BODY}; font-size: 12px;
                             font-weight: 600; color: {TEXT_SECONDARY};">
                    Proposed by <span style="color: {CHAMPION_GOLD};">{safe_proposer}</span>
                </span>
            </td>
        </tr>
    </table>

    <!-- Rule title -->
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
            <td style="padding: 0 24px 12px; font-family: {FONT_BODY}; font-size: 20px;
                        font-weight: 700; color: {TEXT_PRIMARY}; line-height: 1.3;">
                {safe_title}
            </td>
        </tr>
    </table>

    <!-- Rule description card -->
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
            <td style="padding: 0 24px 20px;">
                <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"
                       style="background-color: {DARK_NAVY}; border: 1px solid {SURFACE_LIGHT};
                              border-radius: 10px; border-left: 4px solid {CHAMPION_GOLD};">
                    <tr>
                        <td style="padding: 16px 20px; font-family: {FONT_BODY}; font-size: 14px;
                                    color: {TEXT_SECONDARY}; line-height: 1.7;">
                            {safe_desc if safe_desc else '<em style="color: ' + TEXT_MUTED + ';">No description provided.</em>'}
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>

    <!-- Voting info -->
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
            <td style="padding: 0 24px 20px; font-family: {FONT_BODY}; font-size: 14px;
                        color: {TEXT_PRIMARY}; line-height: 1.6; text-align: center;">
                Your vote matters! A 2/3 majority is needed to approve this rule change.
            </td>
        </tr>
    </table>

    <!-- CTA -->
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
            <td style="padding: 0 24px 8px;" align="center">
                {generate_button("Vote Now", url)}
            </td>
        </tr>
    </table>
    """

    return wrap_email_html(
        content,
        preheader_text=f"{proposer_name} proposed a new rule in {league_name}: {rule_title}" if league_name else f"{proposer_name} proposed a new rule: {rule_title}"
    )


def generate_rule_proposed_email_plain_text(
    proposer_name: str,
    rule_title: str,
    rule_description: str,
    vote_url: str = None,
    league_name: str = "",
) -> str:
    """Generate plain text version."""
    url = vote_url or XOMPER_URL
    league_line = f"League: {league_name}\n" if league_name else ""
    return (
        f"NEW RULE PROPOSAL\n"
        f"=================\n\n"
        f"{league_line}"
        f"Proposed by: {proposer_name}\n\n"
        f"Title: {rule_title}\n\n"
        f"Description:\n"
        f"{rule_description or 'No description provided.'}\n\n"
        f"Your vote matters! A 2/3 majority is needed to approve this rule change.\n\n"
        f"Vote now: {url}\n\n"
        f"---\n"
        f"Xomper Fantasy Football | xomper.xomware.com"
    )
