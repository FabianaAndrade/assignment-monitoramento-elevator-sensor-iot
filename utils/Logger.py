import logging

class Logger:
    """
    Classe para gerenciar a  emissao de 
    logs da aplicação
    """
    def  __init__(self):
        logging.basicConfig(level=logging.INFO, 
                            format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    def info(self, message):
        self.logger.info(message)
    
    def error(self, message):
        self.logger.error(message)