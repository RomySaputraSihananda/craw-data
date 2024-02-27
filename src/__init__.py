from src.main import EngineRomy

from src.services.dataICC import DataICC

def main():
    cli: EngineRomy = EngineRomy()

    cli.main.add_command(DataICC.main, name='data_icc')
    cli.main()

if(__name__ == '__main__'):
    main()