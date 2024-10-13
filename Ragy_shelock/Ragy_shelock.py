import reflex as rx
import asyncio

class State(rx.State):
    """The app state."""
    img: list[str] = []  # List to store uploaded file names
    result: str = ""
    analysis_type: str = ""
    input_method: str = ""
    uploading: bool = False  # Status of uploading
    progress: int = 0  # Progress of the file upload
    total_bytes: int = 0  # Track the total bytes uploaded
    analysis_ready: bool = False  # To display the Start Analysis button after file upload

    async def handle_upload(self, files: list[rx.UploadFile]):
        """Handle the upload of file(s)."""
        for file in files:
            upload_data = await file.read()  # Simulate file reading
            outfile = rx.get_upload_dir() / file.filename  # Get the path to save the file

            # Save the file to the local directory
            with outfile.open("wb") as f:
                f.write(upload_data)

            # Append the uploaded file name to display
            self.img.append(file.filename)
            self.total_bytes += len(upload_data)  # Update total uploaded bytes

        self.result = "File(s) uploaded successfully!"  # Set result message
        self.analysis_ready = True  # Show the analysis options after upload

    def handle_upload_progress(self, progress: dict):
        """Handle the upload progress."""
        self.uploading = True
        self.progress = round(progress["progress"] * 100)  # Update progress percentage
        if self.progress >= 100:
            self.uploading = False  # Upload completed

    def cancel_upload(self):
        """Cancel the file upload."""
        self.uploading = False
        return rx.cancel_upload("upload1")

    def set_analysis_type(self, analysis_type: str):
        """Set the selected analysis type."""
        self.analysis_type = analysis_type

    async def start_analysis(self):
        """Trigger the analysis based on the selected type."""
        if self.analysis_type:
            self.result = f"Starting {self.analysis_type}..."
            
            # API URL based on the analysis type
            api_url = {
                "Code Quality Analysis": "/analyze/quality/",
                "Bug Detection": "/analyze/bugs/",
                "Performance Optimization": "/analyze/performance/",
                "Security Audit": "/analyze/security/",
                "Code Refactoring": "/analyze/refactor/"
            }.get(self.analysis_type, "")

            if api_url:
                # Send HTTP request to the FastAPI backend
                response = await rx.http.get(api_url)
                
                # Handle response
                if response.status_code == 200:
                    self.result = f"Analysis completed: {response.json()}"
                else:
                    self.result = f"Error during {self.analysis_type}: {response.text}"
        else:
            self.result = "Please select an analysis type first."

def input_method_options() -> rx.Component:
    """UI component to choose the input method."""
    return rx.box(
        rx.text("Choose Input Method", font_size="20px", font_weight="bold", color="white"),
        rx.radio_group(
            items=["Upload Files", "Connect GitHub"],
            on_change=State.set_input_method,
            default_value="Upload Files",
            direction="horizontal",
            margin="10px",
            color="white"
        ),
        margin_bottom="20px"
    )

def analysis_options() -> rx.Component:
    """UI component to choose analysis type."""
    return rx.box(
        rx.text("Choose Analysis Type", font_size="20px", font_weight="bold", color="white"),
        rx.radio_group(
            items=["Code Quality Analysis", "Bug Detection", "Performance Optimization", "Security Audit", "Code Refactoring"],
            on_change=State.set_analysis_type,
            default_value="Code Quality Analysis",
            direction="vertical",
            margin="10px",
            color="white"
        ),
    )

def upload_page() -> rx.Component:
    """UI for the file upload, analysis selection, and displaying upload progress."""
    return rx.container(
        rx.vstack(
            # Heading and Description
            rx.text("Comprehensive Code Analysis Tool", font_size="36px", font_weight="bold", color="white", padding="20px"),
            rx.text(
                "Upload your files, choose an analysis, and start analyzing your codebase for quality, bugs, and more.", 
                font_size="18px", color="white", margin_bottom="30px"
            ),
            
            # File Upload Section
            rx.upload(
                rx.vstack(
                    rx.button("Select File", color="white", bg="blue", border="1px solid white"),
                    rx.text("Drag and drop files here or click to select files", color="white"),
                ),
                id="upload1",
                border="2px dashed white",
                padding="5em",
            ),

            # Upload button with progress handling
            rx.hstack(
                rx.button(
                    "Upload Files",
                    on_click=State.handle_upload(rx.upload_files(upload_id="upload1", on_upload_progress=State.handle_upload_progress)),
                    color_scheme="green",
                    margin_top="20px"
                ),
                rx.button(
                    "Cancel Upload",
                    on_click=State.cancel_upload,
                    color_scheme="red",
                    margin_top="20px"
                ),
            ),

            # Progress bar for upload
            rx.progress(value=State.progress, max=100, margin_top="10px", color="green"),
            rx.text("Total bytes uploaded: ", State.total_bytes, color="white", margin_top="20px"),

            # Display upload result
            rx.cond(
                State.result != "",
                rx.text(State.result, font_size="18px", color="green", margin_top="20px"),
            ),

            # Analysis Options (display after successful file upload)
            rx.cond(
                State.analysis_ready,
                rx.vstack(
                    analysis_options(),
                    rx.button(
                        "Start Analysis", 
                        on_click=State.start_analysis, 
                        color_scheme="blue", 
                        margin_top="20px"
                    ),
                )
            ),

            # Display selected analysis and result
            rx.cond(
                State.result != "",
                rx.text(State.result, font_size="18px", color="green", margin_top="20px"),
            ),

            # Spacing and Padding
            padding="2em",
            margin="auto",
            align_items="center",
            background="linear-gradient(to right, #283048, #859398)",  # Full-screen background
            min_height="100vh",
            width="100%",
        )
    )

def index() -> rx.Component:
    """Main index view."""
    return upload_page()

# Initialize the app and add pages
app = rx.App()
app.add_page(index, title="Comprehensive Code Analysis Tool")
