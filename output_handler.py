# Rafael Dewes 2021

class WriteOutput:
    def __init__(self, outputfile):
        self.file = outputfile

    def write_header(self, content):
        try:
            output = open(self.file, 'a')
        except:
            print("Could not open file "+self.file)
            return
        output.write("## Output for "+content)
        output.write("\n")
        output.close()

    def output(self, content, comment=""):
        try:
            output = open(self.file, 'a')
        except:
            print("Could not open file "+self.file)
            return
        
        if len(comment)>1:
            output.write(comment)
            output.write("\n")

        output.write(content)
        output.write("\n")
        
        output.close()

