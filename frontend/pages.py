import reflex as rx

def select_operation():
    """Home page where users can select what type of operation they want to perform."""
    return rx.box(
        rx.heading("Welcome to the Compliance & Anomaly Detection Tool", size="xl", color="blue.500", margin="20px"),
        rx.text("Please select the operation you want to perform:", margin="10px"),
        rx.button("Financial Fraud Detection", on_click=lambda: rx.set_state("financial_fraud"), color_scheme="blue", margin="10px"),
        rx.button("Compliance Check (Not Yet Implemented)", on_click=lambda: rx.set_state("compliance_check"), color_scheme="green", margin="10px"),
        rx.button("Internal Application Compliance (Not Yet Implemented)", on_click=lambda: rx.set_state("internal_compliance"), color_scheme="purple", margin="10px"),
        rx.button("Other Metrics (Coming Soon)", on_click=lambda: rx.set_state("other_metrics"), color_scheme="orange", margin="10px"),
    )

def financial_fraud_page():
    """Page for Financial Fraud Detection."""
    return rx.box(
        rx.heading("Financial Fraud Detection", size="lg", margin="20px"),
        rx.input(placeholder="Enter Transaction ID", id="transaction_id_input", width="50%", margin="10px"),
        rx.button("Check Transaction", on_click=lambda: process_transaction(rx.get_value('transaction_id_input')), color_scheme="blue", margin="20px"),
        rx.text("Result", size="md", margin="20px"),
        rx.text(id="transaction_result", margin="10px", border="1px solid #ccc", padding="10px"),
        rx.button("Download Report", on_click=lambda: download_report(rx.get_value('transaction_id_input')), color_scheme="green", margin="10px")
    )

def compliance_check_page():
    """Placeholder page for Compliance Check (not yet implemented)."""
    return rx.box(
        rx.heading("Compliance Check", size="lg", margin="20px"),
        rx.text("This feature will be implemented in a future release.", margin="10px"),
    )

def internal_compliance_page():
    """Placeholder page for Internal Compliance (not yet implemented)."""
    return rx.box(
        rx.heading("Internal Application Compliance", size="lg", margin="20px"),
        rx.text("This feature will be implemented in a future release.", margin="10px"),
    )

def other_metrics_page():
    """Placeholder for future metrics-related features (not yet implemented)."""
    return rx.box(
        rx.heading("Other Metrics", size="lg", margin="20px"),
        rx.text("This feature will be implemented in a future release.", margin="10px"),
    )

# Router to switch between different operation pages
def app_router():
    """Handles routing based on the user selection."""
    if rx.get_state() == "financial_fraud":
        return financial_fraud_page()
    elif rx.get_state() == "compliance_check":
        return compliance_check_page()
    elif rx.get_state() == "internal_compliance":
        return internal_compliance_page()
    elif rx.get_state() == "other_metrics":
        return other_metrics_page()
    else:
        return select_operation()
