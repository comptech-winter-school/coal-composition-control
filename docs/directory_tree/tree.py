import os
import fnmatch

class TikzTreeProducer:

    def __init__(self):
        self.patterns = []
        self.include_hidden = False
        self.style_name = "horizontal"
        self.escapes = {}

    def get_tree(self, root_dir):
        print(self.tree_header())
        tree = os.walk(root_dir)
        level_not_closed = -1
        for (root, dirs, files) in tree :
            root = root[len(root_dir):]
            if( not self.include_hidden ) :
                dirs[:] = [d for d in dirs if not d[0] == '.']
            current_level = root.count( os.sep )
            if( current_level <= level_not_closed ):
                self.close_nodes( level_not_closed, current_level )
                level_not_closed = current_level
            else :
                level_not_closed += 1
            self.indent_node( current_level, self.open_dir( self.escape( os.path.basename( root ) ) ) )
            f_match = lambda f_name : any(fnmatch.fnmatch( f_name, p ) for p in self.patterns)
            for f in filter(f_match, files):
                self.indent_node( current_level + 1, self.open_file( self.escape( f ) ) )
        else :
            self.close_nodes( level_not_closed, 0 )
        print(self.tree_trailer())

    def open_dir(self, name):
        return f'[{name}, dir'

    def close_nodes(self, fromN, toN) :
        for i in range(fromN, toN - 1, -1):
            self.indent_node(i, ']')

    def escape(self, name):
        for (char, replacement) in self.escapes.items():
            name = name.replace(char, replacement)
        return name

    def indent_node(self, level, name):
        print( 4 * level * ' ' + name )

    def open_file(self, name) :
        return f'[{name}, file]'

    def tree_header(self):
        return r'\begin{forest} for tree={' + self.style_name + '}'

    def tree_trailer(self):
        return r'\end{forest}'


if(__name__ == "__main__") :
    t = TikzTreeProducer()
    t.patterns = ["*.py", "*.md",]
    t.escapes = {'_' : r'$\textunderscore$'}

    t.get_tree("/home/lrdprdx/projects/winter_school/coal-composition-control")
