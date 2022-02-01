import os
import fnmatch

class TikzTreeProducer:

    def __init__(self):
        self.patterns = []
        self.escapes = {}

    def get_tree(self, root_dir):
        tree = os.walk(root_dir)
        level_not_closed = -1
        for (root, _, files) in tree :
            current_level = root.count( os.sep )
            if( current_level <= level_not_closed ) :
                self.close_nodes( level_not_closed, current_level )
                level_not_closed = current_level
            else :
                level_not_closed += 1
            self.indent_node( current_level, self.open_node( self.escape( os.path.basename( root ) ) ) )
            f_match = lambda f_name : any(fnmatch.fnmatch( f_name, p ) for p in self.patterns)
            for f in filter(f_match, files):
                self.indent_node( current_level + 1, self.open_close_node( self.escape( f ) ) )
        else :
            self.close_nodes( level_not_closed, 0 )

    def open_node(self, name):
        return '[' + name

    def close_nodes(self, fromN, toN) :
        for i in range(fromN, toN - 1, -1):
            self.indent_node(i, ']')

    def escape(self, name):
        for (char, replacement) in self.escapes.items():
            name = name.replace(char, replacement)
        return name

    def indent_node(self, level, name):
        print( 4 * level * ' ' + name )

    def open_close_node(self, name) :
        return '[' + name + ']'


if(__name__ == "__main__") :
    t = TikzTreeProducer()
    t.patterns = ["*.py", "*.md"]
    t.escapes = {'_' : r'$\textunderscore$'}

    t.get_tree("..")
