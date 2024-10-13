import reflex as rx

class State(rx.State):
    """The app state."""
    img: list[str] = []
    result: str = ""
    analysis_type: str = ""
    input_method: str = ""
    uploading: bool = False
    progress: int = 0
    total_bytes: int = 0

    async def handle_upload(self, files: list[rx.UploadFile]):
        for file in files:
            upload_data = await file.read()
            outfile = rx.get_upload_dir() / file.filename
            with outfile.open("wb") as f:
                f.write(upload_data)
            self.img.append(file.filename)
            self.total_bytes += len(upload_data)

    def handle_upload_progress(self, progress: dict):
        self.uploading = True
        self.progress = round(progress["progress"] * 100)
        if self.progress >= 100:
            self.uploading = False

    def cancel_upload(self):
        self.uploading = False
        return rx.cancel_upload("upload1")

    def set_analysis_type(self, analysis_type: str):
        self.analysis_type = analysis_type

    def set_input_method(self, method: str):
        self.input_method = method

def input_method_options() -> rx.Component:
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
    return rx.container(
        rx.vstack(
            # Heading and Description
            rx.text("Comprehensive Code Analysis Tool", font_size="36px", font_weight="bold", color="white", padding="20px"),
            rx.text(
                "Analyze your codebase for quality, bugs, performance, and more. Upload your files or connect your GitHub repository.", 
                font_size="18px", color="white", margin_bottom="30px"
            ),
            
            # Input Method Selection
            input_method_options(),

            # Conditionally display file upload or GitHub connection
            rx.cond(
                State.input_method == "Upload Files",
                rx.upload(
                    rx.vstack(
                        rx.button("Select File", color="white", bg="blue", border="1px solid white"),
                        rx.text("Drag and drop files here or click to select files", color="white"),
                    ),
                    id="upload1",
                    border="2px dashed white",
                    padding="5em",
                ),
                # Placeholder for GitHub Integration
                rx.container(
                    rx.text("Connect your GitHub account for code analysis.", color="white"),
                    rx.button("Connect GitHub", color="white", bg="green", padding="10px 20px", margin="10px")
                )
            ),

            # Analysis Options
            analysis_options(),

            # Buttons for processing or canceling
            rx.hstack(
                rx.button(
                    "Process",
                    on_click=State.handle_upload(rx.upload_files(upload_id="upload1")),
                    color_scheme="green",
                    margin_top="20px"
                ),
                rx.button(
                    "Cancel",
                    on_click=State.cancel_upload,
                    color_scheme="red",
                    margin_top="20px"
                ),
            ),
            
            # Progress and Upload Status
            rx.progress(value=State.progress, max=100, margin_top="10px", color="green"),
            rx.text("Total bytes uploaded: ", State.total_bytes, color="white", margin_top="20px"),
            
            # Display result
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
    return upload_page()

# Initialize the app and add pages
app = rx.App()
app.add_page(index, title="Comprehensive Code Analysis Tool")
