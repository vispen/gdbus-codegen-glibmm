class Parser:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.annotations = []

    def post_process(self):
     	print("start")

class Common:
    @staticmethod
    def cppSignatureForDbusSignature(sig):
        """
        The returned tuple has the following values, in order:
            - Type for "in"-parameter to generated function
            - Type for "out" parameter to generated function
            - Type for use with D-Bus function
            - function for casting D-Bus type to out-type
            - function for casting out-type to D-Bus type
        """
        if sig == 'b':
            return ('bool', 'bool', 'bool', "", "")
        elif sig == 'y':
            return ('guchar', 'guchar', 'guchar', "", "")
        elif sig == 'n':
            return ('gint16', 'gint16', 'gint16', "", "")
        elif sig == 'q':
            return ('guint16', 'guint16', 'guint16', "", "")
        elif sig == 'i':
            return ('gint32', 'gint32', 'gint32', "", "")
        elif sig == 'u':
            return ('guint32', 'guint32', 'guint32', "", "")
        elif sig == 'x':
            return ('gint64', 'gint64', 'gint64', "", "")
        elif sig == 't':
            return ('guint64', 'guint64', 'guint64', "", "")
        elif sig == 'd':
            return ('double', 'double', 'double', "", "")
        elif sig == 's':
            return ('std::string', 'std::string', 'Glib::ustring', "Glib::ustring", "")
        elif sig == 'o':
            return ('std::string', 'std::string', 'Glib::ustring', "", "")
        elif sig == 'g':
            return ('std::string', 'std::string', 'Glib::ustring', "", "")
        else:
            return (None, None, None, None, None)     	
     	

class Arg:
	def __init__(self, name, signature):
		self.name = name
		self.signature = signature
		self.annotations = []

	def parens(self, expr):
		if not expr:
			return

		self.parens(expr[expr.find('(', 1):expr.rfind(')', 0, len(expr)-1)+1])
	
	def post_process(self):
		self.parens("(sa{sv})")
		
		print("-----new function-----")
		ans = self.parse("as")
		print(ans)

	def parse(self, expr):
		
		#print(expr)
		#base case
		if not expr:
			return

		#Check if struct or dictionary before proceding
		if expr[0] == '(':
			return
		elif expr[0] == '{':
			return
		elif expr[0] == 's':
			return ('std::string', 'std::string', 'Glib::ustring', "Glib::ustring", "")
		elif expr[0] == 'a':
			ret = self.parse(expr[1:])
			lst = list(ret)
			lst[0] = 'std::vector<'+ lst[0] +'>'
			lst[1] = 'std::vector<'+ lst[1] +'>'
			lst[2] = 'std::vector<'+ lst[2] +'>'
			lst[3] = 'function for casting D-Bus type to out-type'
			lst[4] = 'function for casting out type to D-Bus type'
			return tuple(lst) 
		else:
			return self.parse(expr[1:])
				

b = Arg("userProfile", "(sa{sv})")
b.post_process()




