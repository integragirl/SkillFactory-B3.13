class Tag:
    def __init__(self, tag, klass=None, is_single=False, **kwargs):
        self.tag = tag

        self.text = ""
        self.attributes = {}

        self.toplevel = False
        self.is_single = is_single
        self.children = []

        if klass is not None:
            self.attributes["class"] = " ".join(klass)

        for attr, value in kwargs.items():
            if "_" in attr:
                attr = attr.replace("_", "-")
            self.attributes[attr] = value

    def __enter__(self):
        return self

    def __add__(self, children_plus):
        self.children.append(children_plus)
        return self

    def __exit__(self, type, value, traceback):
        if self.toplevel:
            print("<%s>" % self.tag)
            for child in self.children:
                print(child)

            print("</%s>" % self.tag)

    def __str__(self):
        #print('Tag')
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append('%s="%s"' % (attribute, value))
        attrs = " ".join(attrs)

        if self.children:
            opening = "<{tag} {attrs}>".format(tag=self.tag, attrs=attrs)
            internal = "%s" % self.text
            for child in self.children:
                internal += str(child)
            ending = "</%s>" % self.tag
            return opening + internal + ending
        else:
            if self.is_single:
                return "<{tag} {attrs}/>".format(tag=self.tag, attrs=attrs)

            else:
                return "<{tag} {attrs}>{text}</{tag}>".format(
                    tag=self.tag, attrs=attrs, text=self.text
                )

class HTML():
    def __init__(self, output):
        self.tag = 'HTML'
        self.output = None
        self.children = []
        self.toplevel = True

    def __enter__(self):
        return self

    def __add__(self, children_plus):
        self.children.append(children_plus)
        return self

    def __exit__(self, type, value, traceback):
        if self.toplevel:
            print("<%s>" % self.tag)
            for child in self.children:
                print(child)

            print("</%s>" % self.tag)

    def __str__(self):
        #print('HTML')
        if self.children:
            opening = "<{tag}>".format(tag=self.tag)
            internal = ''
            for child in self.children:
                internal += str(child)
            ending = "</%s>" % self.tag
            return opening + internal + ending
        else:
            return "<{tag} {attrs}>{text}</{tag}>".format(
                tag=self.tag, attrs=attrs, text=self.text
            )

class TopLevelTag(Tag):
    def __init__(self, tag):
        self.tag = tag

        self.text = ""
        self.attributes = {}

        self.toplevel = True
        self.children = []

    def __enter__(self):
        return self

    def __add__(self, children_plus):
        self.children.append(children_plus)
        return self

    def __exit__(self, type, value, traceback):
        pass
        #print('TopLevelTag exit')

    def __str__(self):
        #print('TopLevelTag')
        if self.children:
            opening = "<{tag}>".format(tag=self.tag)
            internal = "%s" % self.text
            for child in self.children:
                internal += str(child)
            ending = "</%s>" % self.tag
            return opening + internal + ending
        else:
            if self.is_single:
                return "<{tag}/>".format(tag=self.tag)

            else:
                return "<{tag}>{text}</{tag}>".format(
                    tag=self.tag, text=self.text
                )


if __name__ == "__main__":

    with HTML(output=None) as doc:
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "hello"
                head += title
            doc += head
        
        with TopLevelTag("body") as body:
            
            with Tag("h1", klass=("main-text",)) as h1:
                h1.text = "Test"
                body += h1

            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                with Tag("p") as paragraph:
                    paragraph.text = "another test"
                    div += paragraph

                with Tag("img", is_single=True, src="/icon.png") as img:
                    div += img

                body += div

            doc += body