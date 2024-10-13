from frontend.pages import app_router
import reflex as rx

# Define the Reflex app
class ScalableApp(rx.App):
    def build(self):
        return rx.page(app_router())

if __name__ == "__main__":
    ScalableApp().run()
