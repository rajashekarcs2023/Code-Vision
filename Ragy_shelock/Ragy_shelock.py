import reflex as rx

class State(rx.State):
    """The app state."""
    img: list[str] = []  # List to store uploaded image file names
    uploading: bool = False  # Status of uploading
    progress: int = 0  # Progress of the file upload
    total_bytes: int = 0  # Track the total bytes uploaded
    selected_knowledge_base: str = "fraud_prevention"  # Default selected knowledge base
    compliance_report: str = ""  # Placeholder for compliance report

    async def handle_upload(self, files: list[rx.UploadFile]):
        """Handle the upload of file(s).

        Args:
            files: The uploaded files.
        """
        for file in files:
            upload_data = await file.read()  # Read the file data
            outfile = rx.get_upload_dir() / file.filename  # Get the path to save the file

            # Save the file to the directory
            with outfile.open("wb") as f:
                f.write(upload_data)

            # Append the uploaded file name to the img list to display
            self.img.append(file.filename)
            self.total_bytes += len(upload_data)

    def handle_upload_progress(self, progress: dict):
        """Handle the upload progress.

        Args:
            progress: Dictionary containing progress information.
        """
        self.uploading = True
        self.progress = round(progress["progress"] * 100)  # Update progress percentage
        if self.progress >= 100:
            self.uploading = False  # Upload completed

    def cancel_upload(self):
        """Cancel the file upload."""
        self.uploading = False
        return rx.cancel_upload("upload1")

    def process_transactions(self):
        """Simulate processing the uploaded transactions."""
        if not self.img:
            self.compliance_report = "No file uploaded to process."
        else:
            self.compliance_report = f"Compliance report based on {self.selected_knowledge_base} generated!"

    def download_report(self):
        """Simulate downloading the compliance report."""
        return rx.download("compliance_report.txt", content=self.compliance_report)

    def set_knowledge_base(self, kb: str):
        """Set the selected knowledge base."""
        self.selected_knowledge_base = kb

# Color for styling
color = "rgb(107,99,246)"

def upload_page() -> rx.Component:
    """UI for the file upload and displaying images."""
    return rx.vstack(
        # Select knowledge base
        rx.select(
            items=["fraud_prevention", "regulatory_compliance", "industry_guidelines"],
            value=State.selected_knowledge_base,
            on_change=lambda kb: State.set_knowledge_base(kb),
            placeholder="Select Knowledge Base"
        ),

        # File upload area with drag and drop support
        rx.upload(
            rx.vstack(
                rx.button("Select File", color=color, bg="white", border=f"1px solid {color}"),
                rx.text("Drag and drop files here or click to select files"),
            ),
            id="upload1",  # Assigning ID to the upload component
            border=f"1px dotted {color}",
            padding="5em",
        ),

        # Display selected files before upload
        rx.hstack(rx.foreach(rx.selected_files("upload1"), rx.text)),

        # Progress bar for the upload
        rx.progress(value=State.progress, max=100),

        # Upload button - this is where progress is handled
        rx.cond(
            ~State.uploading,  # If not uploading, show the Upload button
            rx.button(
                "Upload", 
                on_click=State.handle_upload(rx.upload_files(upload_id="upload1", on_upload_progress=State.handle_upload_progress))  # Handle upload progress
            ),
            # If uploading, show the Cancel button
            rx.button(
                "Cancel", 
                on_click=State.cancel_upload
            ),
        ),

        # Process Transactions button
        rx.button(
            "Process Transactions", 
            on_click=State.process_transactions, 
            color_scheme="blue", 
            margin_top="20px"
        ),

        # Display compliance report result
        rx.cond(
            State.compliance_report != "",
            rx.text(State.compliance_report, size="5", margin_top="20px"),
        ),

        # Download Compliance Report button
        rx.button(
            "Download Compliance Report", 
            on_click=State.download_report, 
            color_scheme="green", 
            margin_top="20px"
        ),

        # Display uploaded images and filenames
        rx.foreach(State.img, lambda img: rx.image(src=rx.get_upload_url(img))),

        # Total uploaded bytes displayed
        rx.text("Total bytes uploaded: ", State.total_bytes),
        padding="5em",
    )

# Main routing function
def index() -> rx.Component:
    """Main index view."""
    return upload_page()

# Initialize the app and add pages
app = rx.App()
app.add_page(index, title="File Upload with Knowledge Base Selection and Compliance Report")
