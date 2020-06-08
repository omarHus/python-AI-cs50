import sys

from crossword import *
from copy import deepcopy


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        # self.initialize_assignment()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # Only keep values that are the same length as variable
        for var in self.domains.keys():
            self.domains[var] = { value for value in self.domains[var] if len(value) == var.length }


    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        
        # find the constraints for (x,y)
        constraints = self.crossword.overlaps[x, y]
        if constraints is not None:
            # Check each x_val to see if it satisfies binary constraints
            for x_val in list(self.domains[x]):
                satisfied = False
                for y_val in self.domains[y]:
                    # Check if intersection of x and y match
                    if y_val[constraints[1]] == x_val[constraints[0]]:
                        satisfied = True
                        break
                # if no y_val in y domain satisfies this constraint then remove x_val from x domain
                if not satisfied:
                    self.domains[x].remove(x_val)
                    revised = True
        return revised
            


    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        queue = arcs
        if queue is None:
            # make an initial list of all the arcs in the problem
            queue = list(self.crossword.overlaps)

        
        while len(queue) > 0:
            (x, y) = queue.pop()
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for neighbor in self.crossword.neighbors(x)-{y}:
                    next_in_queue = (neighbor, x)
                    queue.append(next_in_queue)
        return True




    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        if len(assignment) < len(self.domains):
            return False

        for value in assignment.values():
            if value is None:
                return False
    
        return True



    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        # all values must be distinct, correct length, and no conflicts between neighboring values
        test_set = set()
        for v1, value in assignment.items():
            if v1.length != len(value):
                return False

            if value in test_set:
                return False
            test_set.add(value)

            # check for conflicting characters
            for neighbor in self.crossword.neighbors(v1):
                i, j = self.crossword.overlaps[v1, neighbor]
                try:
                    value2 = assignment[neighbor]
                    if value[i] != value2[j]:
                        return False
                except:
                    # do nothing
                    print("not assigned")
                

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        
        # return arbitrary ordering for now
        return self.domains[var]


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        for var in self.domains.keys():
            if var not in assignment.keys():
                return var
    

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        
        # Return complete assignment
        if self.assignment_complete(assignment):
            return assignment
        
        # Select an unassigned variable and assign a consistent value
        var = self.select_unassigned_variable(assignment)
        
        
        for value in self.domains[var]:
            # Try assigning value to var and see if its consistent
            assignment[var] = value
            if self.consistent(assignment):
                # Keep assignment and backtrack recursively
                result = self.backtrack(assignment)
                if result is not None:
                    return result
            # If assignment didnt work then remove it
            assignment.pop(var)
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
