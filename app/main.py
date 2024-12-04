import logging

from tkinterdnd2 import TkinterDnD

from app.controller.PDFProcessingController import PDFProcessingController
from app.data_extractor.land_register_data_extractor import LandRegisterDataExtractor
from app.data_extractor.ownership_factory.company_ownership_factory import CompanyOwnershipFactory
from app.data_extractor.ownership_factory.ownership_dispatcher import OwnershipDispatcher
from app.data_extractor.ownership_factory.private_ownership_factory import PrivateOwnershipFactory
from app.logger.logger_factory import LoggerFactory
from app.view.main_window import MainWindow




def main():
    logger_factory = LoggerFactory(log_dir='../logs', enable_console=True)

    # Get a logger instance
    logger = logger_factory.get_logger(name='PDFProcessor', log_file_name='pdf_processor.log', level=logging.DEBUG)

    try:
        logger.info("Starting PDFProcessor application")

        root = TkinterDnD.Tk()
        logger.info("TkinterDnD root initialized")

        # Initialize components
        logger.info("Initializing extractors")
        company_ownership_factory = CompanyOwnershipFactory(logger)
        private_ownership_factory = PrivateOwnershipFactory(logger)
        ownership_dispatcher = OwnershipDispatcher(private_ownership_factory, company_ownership_factory, logger)
        land_register_extractor = LandRegisterDataExtractor(ownership_dispatcher, logger)

        logger.info("Initializing controller")
        controller = PDFProcessingController(land_register_extractor, logger)

        # Create and attach the application GUI to the root
        logger.info("Initializing application GUI")
        app = MainWindow(root, controller)
        root.app = app  # Explicitly attach the app instance to the root
        logger.info("Application GUI initialized successfully")

        root.mainloop()
        logger.info("Application terminated")


    except Exception as e:
        logger.critical(f"Failed to initialize the application: {e}", exc_info=True)


if __name__ == "__main__":
    main()
