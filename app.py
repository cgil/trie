from trie import create_app
from trie.utils.configuration import config

if __name__ == '__main__':
    app = create_app()
    app.run(debug=config.get('debug'))
