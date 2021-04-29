class Sheet:
    def __init__(self):
        self.md = open("test_results/sheet.md", "a")

    def clear(self):
        self.md.close()
        self.md = open("test_results/sheet.md", "w")
        self.md.write("")
        self.md.close()
        self.md = open("test_results/sheet.md", "a")

    def title(self, titletext):
        self.md.write("# {}\n".format(titletext))

    def subtitle(self, subt):
        self.md.write("## {}\n".format(subt))

    def union_1(self, image_name, hval, signature, v, psnr):
        self.md.write("|{}|{}|\n".format("Property", "Value"))
        self.md.write("|--|--|\n")
        # self.md.write("|Signed Image|![](./{}-signed.png)|\n".format(image_name))
        el = '<img src="./NAME-signed.png" alt="NAME" width="200"/>'.replace("NAME", image_name)
        self.md.write("|Signed Image|{}|\n".format(el))
        self.md.write("|{}|{}|\n".format("Hash", hval))
        self.md.write("|{}|{}|\n".format("Sign", signature))
        self.md.write("|{}|{}|\n".format("PSNR", psnr))
        self.md.write("|{}|{}|\n".format("Verify", v))
        self.md.write("  \n")

    def paragraph(self, para):
        self.md.write("{}\n  \n".format(para))

    def __del__(self):
        self.md.close()

