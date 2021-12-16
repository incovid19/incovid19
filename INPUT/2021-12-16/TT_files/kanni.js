(function() {
	if (!window.Kanni) {
		window.Kanni = {
			language : "en",
			method : "",
			_planguage : "en",
			_pmethod : "",
			languages : {},
			switchkey : 120,
			_activeelement : null,
			showtips : true,
			ignoreevents : false,
			attachlangswitch : true,
			attachkeyevents : true,
			attachclasses : "form-textarea",
			hidelangswitch : true
		}
	}
	Kanni.init = function() {
		if (typeof kanniConfig == "undefined") {
			kanniConfig = {}
		}
		for ( var e in kanniConfig) {
			Kanni[e] = kanniConfig[e]
		}
		this.switchKey(this.switchkey);
		if (this.attachlangswitch) {
			if ("langswitchdiv" in kanniConfig) {
				this.attachLanguageSwitcher(kanniConfig["langswitchdiv"])
			} else {
				this.attachLanguageSwitcher()
			}
			var t = document.getElementById("kanni-lang-switch");
			if ("language" in kanniConfig && "method" in kanniConfig) {
				var n = {
					language : kanniConfig["language"],
					method : kanniConfig["method"]
				};
				Kanni.langMethod(n)
			} else if (t) {
				Kanni.langMethod(t.value)
			}
			this._attachEvent(document, "keyup", function(e) {
				e = e || event;
				var t = e.which || e.keyCode;
				if (t != Kanni.switchkey) {
					return true
				}
				Kanni.toggle();
				return false
			})
		}
		if (this.attachkeyevents) {
			if (this.attachclasses == "*") {
				var r = document.getElementsByTagName("input");
				for (var i = 0; i < r.length; i++) {
					var s = r[i];
					if (s.type != "text") {
						continue
					}
					Kanni.enableNode(s)
				}
				var r = document.getElementsByTagName("textarea");
				for (var i = 0; i < r.length; i++) {
					var o = r[i];
					Kanni.enableNode(o)
				}
			} else {
				var u = this._getElementsByClass(this.attachclasses);
				for ( var a in u) {
					var f = u[a];
					Kanni.enableNode(f)
				}
			}
			var u = this._getElementsByClass("kanni-enabled");
			for ( var a in u) {
				var f = u[a];
				Kanni.enableNode(f)
			}
		}
	};
	Kanni.digest = function(e, t, n, r) {
		if (!r) {
			r = {
				language : this.language,
				method : this.method
			}
		}
		config = Kanni.langConfig(r);
		if (!config) {
			return false
		}
		var i = "";
		var s = "";
		var o = "";
		var u = "";
		var a = 0;
		var f = 4;
		if ("maxchar" in config.method) {
			f = config.method.maxchar
		}
		if (n <= 0) {
			i = "";
			o = t
		} else {
			i = t.substring(0, n);
			o = t.substring(n)
		}
		if (i.length > 0) {
			for (var l = i.length - 1; l >= 0; l--) {
				var c = i.charAt(l);
				var h = i.charCodeAt(l);
				if (h <= 127) {
					break
				}
				a++;
				if (a >= f) {
					break
				}
			}
		}
		if (a >= i.length) {
			s = i;
			i = ""
		} else {
			var p = i.length - a;
			if (p <= 0) {
				p = 0
			}
			s = i.substring(p);
			i = i.substring(0, p)
		}
		u = this.map(e, s, r);
		return {
			left : i,
			prev : s,
			"new" : u,
			right : o
		}
	};
	Kanni.map = function(e, t, n) {
		var r = t + e;
		var i = Kanni.langConfig(n);
		if (i) {
			var s = i.method.charmap;
			for ( var o in s) {
				rexp = new RegExp(o, "g");
				r = r.replace(rexp, s[o])
			}
		}
		return r
	};
	Kanni.keyPressHandler = function(e) {
		var t = e.target || e.srcElement;
		var n = t.ownerDocument;
		return Kanni.KeyPressProcessor(e, t, n)
	};
	Kanni.KeyPressProcessor = function(e, t, n) {
		var r = e.keyCode || e.which;
		var i = 0;
		if (Kanni.language == "en") {
			return true
		}
		var s = {
			language : this.language,
			method : this.method
		};
		if (!Kanni.keyValidator(e, s)) {
			return true
		}
		var o = String.fromCharCode(r);
		result = this.process(o, t, n, s);
		if (e.preventDefault) {
			e.preventDefault();
			e.stopPropagation()
		} else {
			e.returnValue = false;
			e.cancelBubble = true
		}
		if (this.tips()) {
			this.showTips(result["new"])
		}
		return false
	};
	Kanni.process = function(e, t, n, r, i) {
		if (typeof i == "undefined") {
			i = true
		}
		var s = [ "text", "search", "url" ];
		if (t.nodeName.toLowerCase() == "textarea"
				|| t.nodeName.toLowerCase() == "input"
				&& s.indexOf(t.type.toLowerCase()) != -1) {
			var o = t.value;
			if ("selectionStart" in t) {
				offset = t.selectionStart
			} else {
				range = document.selection.createRange();
				if (range && range.parentElement() == t) {
					var u = t.value.length;
					var a = t.value.replace(/\r\n/g, "\n");
					var f = t.createTextRange();
					f = f.duplicate();
					f.moveToBookmark(range.getBookmark());
					var l = t.createTextRange();
					l.collapse(false);
					if (f.compareEndPoints("StartToEnd", l) > -1) {
						start = end = u
					} else {
						start = -f.moveStart("character", -u);
						start += a.slice(0, start).split("\n").length - 1;
						if (f.compareEndPoints("EndToEnd", l) > -1) {
							end = u
						} else {
							end = -f.moveEnd("character", -u);
							end += a.slice(0, end).split("\n").length - 1
						}
					}
				}
				offset = start
			}
			var c = Kanni.digest(e, o, offset);
			var h = c["left"] + c["new"] + c["right"];
			t.value = h;
			var a = c["left"] + c["new"];
			a = a.replace(/\r\n/g, "1");
			offset = a.length;
			if ("selectionStart" in t) {
				t.selectionStart = offset;
				t.selectionEnd = offset
			} else if ("setSelectionRange" in t) {
				field.setSelectionRange(offset, offset)
			} else if ("createTextRange" in t) {
				var f = t.createTextRange();
				f.move("character", offset);
				f.moveEnd("character", 0);
				f.collapse(false);
				f.select()
			}
		} else {
			if (n.getSelection) {
				selection = n.getSelection();
				range = selection.getRangeAt(0)
			} else if (n.selection && n.selection.createRange) {
				selection = n.selection;
				range = n.selection.createRange()
			}
			if ("startContainer" in range) {
				offset = range.startOffset;
				t = range.startContainer
			} else {
				var d = range.duplicate();
				rng2 = range.duplicate();
				rng2.moveToElementText(d.parentElement());
				rng2.setEndPoint("EndToStart", d);
				offset = rng2.text.length;
				var v = range.duplicate();
				var m = range.duplicate();
				v.collapse(true);
				v.moveEnd("character", 1);
				var g = v.parentElement();
				m.moveToElementText(g);
				m.setEndPoint("EndToEnd", v);
				var y = m.text;
				var b = null;
				if (g.childNodes.length > 0) {
					for (var w = 0; w < g.childNodes.length; w++) {
						tnode = g.childNodes[w];
						if (tnode.nodeType == 3) {
							var E = tnode.nodeValue;
							var S = y.indexOf(E);
							if (S == 0 && y != E) {
								y = y.substring(E.length)
							} else {
								b = tnode;
								break
							}
						}
					}
				}
				t = b;
				if (!t) {
					t = g
				}
			}
			offsetplus = 0;
			if (t.nodeType == 3) {
				nodevalue = t.nodeValue;
				oldprevstr = "";
				oldnextstr = "";
				if (t.parentNode) {
					pnode = t.parentNode;
					currhtml = pnode.innerHTML;
					if (currhtml.length > 4) {
						E = currhtml.substring(currhtml.length - 4);
						if (E == "<BR>") {
							oldprevstr = nodevalue;
							nodevalue = "\r\n";
							offsetplus += 2
						}
						E = currhtml.substring(0, 4);
						if (E == "<BR>") {
							oldnextstr = nodevalue;
							nodevalue = "\r\n"
						}
					}
				}
				c = Kanni.digest(e, nodevalue, offset);
				h = c["left"] + c["new"] + c["right"];
				if (oldprevstr.length) {
					pnode.innerText = oldprevstr + h
				} else if (oldnextstr.length) {
					pnode.innerText = h + oldnextstr
				} else {
					t.nodeValue = h
				}
			} else {
				c = Kanni.digest(e, "", offset);
				h = c["left"] + c["new"] + c["right"];
				var x = n.createTextNode(h);
				if (t.childNodes.length > 0 && t.childNodes[offset]) {
					t.insertBefore(x, t.childNodes[offset])
				} else if (t.nodeName == "HR") {
					p = t.parentNode;
					p.insertBefore(x, t)
				} else {
					t.appendChild(x)
				}
				t = x
			}
			var a = c["left"] + c["new"];
			a = a.replace(/\r\n/g, "1");
			offset = a.length + offsetplus;
			if ("setStart" in range) {
				range.setStart(t, offset);
				range.setEnd(t, offset);
				selection.removeAllRanges();
				selection.addRange(range)
			} else {
				range.move("character", offset);
				range.moveStart("character", 0);
				range.collapse(true);
				range.select()
			}
		}
		return c
	};
	Kanni.CKEditorKeyPressHandler = function(e, t) {
		if (t.mode != "wysiwyg") {
			return true
		}
		var n = e;
		var r = e.data.$;
		var i = t.document.$;
		Kanni._activeelement = i;
		return Kanni.KeyPressProcessor(r, i, i)
	};
	Kanni.keyValidator = function(e, t) {
		if (e.altKey || e.ctrlKey || e.metaKey) {
			return false
		}
		var n = e.which || e.keyCode;
		if ("charCode" in e && !e.charCode) {
			return false
		}
		if (n < 32 || n >= 127) {
			return false
		}
		var r = String.fromCharCode(n);
		rexp = new RegExp(/[\x00-\x1F\x80-\xFF]/);
		if (rexp.test(r)) {
			return false
		}
		return true
	};
	Kanni.langConfig = function(e) {
		if (!e) {
			e = {
				language : this.language,
				method : this.method
			}
		}
		if (!(e.language in this.languages)) {
			return false
		}
		var t = this.languages[e.language];
		var n = t["methods"];
		if (!(e.method in n)) {
			return false
		}
		var r = n[e.method];
		return {
			language : t,
			method : r
		}
	};
	Kanni.charExistsInMap = function(e, t) {
		var n = this.langConfig(t);
		if (!n) {
			return false
		}
		var r = n.method.charmap;
		for ( var i in r) {
			if (i == e || r[i] == e) {
				return true
			}
			if (r[i].toString().length > 1) {
				for ( var s in r[i].toString()) {
					if (s == e) {
						return true
					}
				}
			}
			if (i.length > 1) {
				for ( var s in i) {
					if (s == e) {
						return true
					}
				}
			}
		}
		return false
	};
	Kanni.insertChar = function(e) {
		var t = this.activeElement();
		if (!t) {
			return
		}
		var n = {
			language : this.language,
			method : this.method
		};
		var r = t.ownerDocument;
		if (!t.ownerDocument) {
			r = t
		}
		this.process(e, t, r, n, false);
		this.ignoreevents = true;
		if ("focus" in t) {
			t.focus()
		}
		this.ignoreevents = false;
		return false
	};
	Kanni.showTips = function(e) {
		if (this.language == "en") {
			return
		}
		if (!this.languages[this.language]["methods"][this.method].mergeprevchar) {
			return
		}
		var t = "aAeEiIoOuU";
		var n = "";
		var r = "";
		var i;
		for (var s = 0; s < t.length; s++) {
			i = t.substr(s, 1);
			result = this.digest(i, e, e.length);
			r = r + "&nbsp;&nbsp;" + result["prev"] + " + " + i + " = <b>"
					+ result["new"] + "</b>"
		}
		var o = document.getElementById("kanni-lang-tips-block");
		o.innerHTML = r;
		this.showTipsDiv()
	};
	Kanni.switchKey = function(e) {
		if (e) {
			this.switchkey = e
		}
		return this.switchkey
	};
	Kanni.langMethod = function(e) {
		if (e) {
			if (typeof e == "string") {
				e = e.split("|");
				e = {
					language : e[0],
					method : e[1]
				}
			} else if (typeof e == "object") {
			} else {
				return false
			}
			this._planguage = this.language;
			this._pmethod = this.method;
			this.language = e.language;
			this.method = e.method;
			select = document.getElementById("kanni-lang-switch");
			if (select) {
				select.value = this.language + "|" + this.method
			}
			this.initKeyboard();
			var t = new Date;
			t.setTime(t.getTime() + 1e3 * 3600 * 24 * 30);
			this._set_cookie("kanni_user_lang", this.language + "|"
					+ this.method, t, "/")
		}
		return {
			language : this.language,
			method : this.method
		}
	};
	Kanni.activeElement = function(e) {
		if (typeof e != "undefined") {
			this._activeelement = e
		}
		return this._activeelement
	};
	Kanni.tips = function(e) {
		if (typeof e != "undefined") {
			this.showtips = e;
			showtips = document.getElementById("kanni-lang-tips");
			showtips.checked = e;
			if (this.showtips) {
				value = 1
			} else {
				value = 0
			}
			var t = new Date;
			t.setTime(t.getTime() + 1e3 * 3600 * 24 * 30);
			this._set_cookie("kanni_user_tips", value, t, "/")
		}
		return this.showtips
	};
	Kanni.toggle = function() {
		if (this.language != "en") {
			this.langMethod("en|en")
		} else {
			this.langMethod({
				language : this._planguage,
				method : this._pmethod
			})
		}
	};
	Kanni.attachLanguageSwitcher = function(e) {
		var t = "";
		if (!e) {
			t = t
					+ "#kanni-lang-switch-block {padding:5px;text-align:left;z-index:99;line-height:1em;position:fixed;width:150px;bottom:0px;left:10px;background:#EDF5FA;border:solid 1px #336699;display:none;}";
			t = t + "#kanni-lang-switch-block select {width:140px}"
		}
		t = t
				+ "#kanni-lang-tips-block{display:none;z-index:99;position:fixed;left:170px;bottom:0px;background-color:#EDF5FA;border:solid 1px #336699}";
		t = t
				+ "#kanni-lang-keyboard-block{display:none;z-index:99;position:fixed;left:165px;bottom:0px;background-color:#EDF5FA;border:solid 1px #336699}";
		var n = document.createElement("style");
		n.type = "text/css";
		if (n.styleSheet) {
			n.styleSheet.cssText = t
		} else {
			n.appendChild(document.createTextNode(t))
		}
		document.getElementsByTagName("head")[0].appendChild(n);
		var r = '<option value="en|en">English</option>';
		var i = this.languages;
		if ("enabledLanguages" in this) {
			i = this.enabledLanguages
		}
		for ( var s in i) {
			var o = this.languages[s];
			for ( var u in i[s].methods) {
				var a = o.methods[u];
				r += '<option value="' + s + "|" + u + '">' + o["name"] + " - "
						+ a.method + "</option>"
			}
		}
		var f = this._get_cookie("kanni_user_tips");
		if (f == "1") {
			f = "checked"
		} else {
			f = ""
		}
		var l = '<label for="kanni-lang-tips">Type Lang</label><input type="checkbox" ' + f
				+ ' id="kanni-lang-tips" /> tips | ';
		var c = '<a href="#" alt="Keyboard" onclick="Kanni.showKeyboard(); return false;">Keyboard</a>';
		var h = '<label for="kanni-lang-switch">Type method</label>'
				+ '<select id="kanni-lang-switch">' + r + "</select>" + "<div>"
				+ l + c + "</div>";
		var p = document.createElement("div");
		p.setAttribute("class", "kanni-lang-switch-block");
		p.setAttribute("id", "kanni-lang-switch-block");
		p.innerHTML = h;
		if (e) {
			e = document.getElementById(e)
		} else {
			e = document.body
		}
		e.appendChild(p);
		var d = document.getElementById("kanni-lang-switch");
		var v = this._get_cookie("kanni_user_lang");
		if (v) {
			this.langMethod(v)
		}
		Kanni._attachEvent(d, "change", function() {
			Kanni.langMethod(d.value)
		});
		showtips = document.getElementById("kanni-lang-tips");
		Kanni._attachEvent(showtips, "click", function() {
			Kanni.tips(showtips.checked)
		});
		var p = document.createElement("div");
		p.setAttribute("class", "kanni-lang-tips-block");
		p.setAttribute("id", "kanni-lang-tips-block");
		e.appendChild(p);
		Kanni._attachEvent(document, "mousemove", function() {
			Kanni.hideTipsDiv()
		});
		var p = document.createElement("div");
		p.setAttribute("class", "kanni-lang-keyboard-block");
		p.setAttribute("id", "kanni-lang-keyboard-block");
		e.appendChild(p);
		return
	};
	Kanni.initKeyboard = function(lang) {
		var keyboard = document.getElementById("kanni-lang-keyboard-block");
		if (!keyboard) {
			return
		}
		if (!lang) {
			lang = {
				language : this.language,
				method : this.method
			}
		}
		for (var idx = 0; idx < keyboard.childNodes.length; idx++) {
			this
					._setStyleAttribute(keyboard.childNodes[idx], "display",
							"none")
		}
		kb = document.getElementById("kanni-kb-" + this.language);
		if (kb) {
			this._setStyleAttribute(kb, "display", "block")
		} else {
			config = this.langConfig(lang);
			if (!config) {
				return
			}
			var charkeyfrom = eval('"\\u' + config.language.charfrom + '"')
					.charCodeAt(0);
			var charkeyto = eval('"\\u' + config.language.charto + '"')
					.charCodeAt(0);
			var buttons = '<a href="#" alt="Keyboard" onclick="Kanni.hideKeyboard();"> X </a>';
			for (var ucharkey = charkeyfrom; ucharkey <= charkeyto; ucharkey++) {
				var char = String.fromCharCode(ucharkey);
				buttons += '<input type="button" class="' + ucharkey
						+ '" value="' + char
						+ '" onclick="Kanni.insertChar(this.value);"/>'
			}
			var node = document.createElement("div");
			node.setAttribute("class", "kanni-kb-" + this.language);
			node.setAttribute("id", "kanni-kb-" + this.language);
			keyboard.appendChild(node);
			node.innerHTML = buttons
		}
	};
	Kanni.showKeyboard = function() {
		var e = document.getElementById("kanni-lang-keyboard-block");
		Kanni._setStyleAttribute(e, "display", "block")
	};
	Kanni.hideKeyboard = function() {
		var e = document.getElementById("kanni-lang-keyboard-block");
		Kanni._setStyleAttribute(e, "display", "none")
	};
	Kanni.showLanguageSwitcher = function(e) {
		if (Kanni.ignoreevents) {
			return
		}
		Kanni.activeElement(e.target || e.srcElement);
		if ("_langswitchtimer_" in Kanni) {
			clearTimeout(Kanni._langswitchtimer_)
		}
		var t = document.getElementById("kanni-lang-switch-block");
		if (typeof jQuery != "undefined") {
			jQuery(t).show("normal");
			return
		}
		Kanni._setStyleAttribute(t, "display", "block")
	};
	Kanni.hideLanguageSwitcher = function() {
		if (Kanni.ignoreevents) {
			return
		}
		if (Kanni.hidelangswitch) {
			Kanni._langswitchtimer_ = setTimeout(
					"Kanni._hideLanguageSwitcher();", 5e3)
		}
	};
	Kanni._hideLanguageSwitcher = function() {
		if ("_langswitchtimer_" in Kanni) {
			clearTimeout(Kanni._langswitchtimer_)
		}
		var e = document.getElementById("kanni-lang-switch-block");
		if (typeof jQuery != "undefined") {
			jQuery(e).hide("normal");
			return
		}
		Kanni._setStyleAttribute(e, "display", "none")
	};
	Kanni.showTipsDiv = function() {
		var e = document.getElementById("kanni-lang-tips-block");
		if (typeof jQuery != "undefined") {
			jQuery(e).show("normal");
			return
		}
		Kanni._setStyleAttribute(e, "display", "block")
	};
	Kanni.hideTipsDiv = function() {
		var e = document.getElementById("kanni-lang-tips-block");
		if (typeof jQuery != "undefined") {
			jQuery(e).hide("normal");
			return
		}
		Kanni._setStyleAttribute(e, "display", "none")
	};
	Kanni._get_cookie = function(e) {
		var t = document.cookie;
		var n = e + "=";
		var r = t.indexOf("; " + n);
		if (r == -1) {
			r = t.indexOf(n);
			if (r != 0) {
				return null
			}
		} else {
			r += 2
		}
		var i = document.cookie.indexOf(";", r);
		if (i == -1) {
			i = t.length
		}
		return unescape(t.substring(r + n.length, i))
	};
	Kanni._set_cookie = function(e, t, n, r, i, s) {
		var o = e + "=" + escape(t) + (n ? "; expires=" + n.toGMTString() : "")
				+ (r ? "; path=" + escape(r) : "") + (i ? "; domain=" + i : "")
				+ (s ? "; secure" : "");
		document.cookie = o
	};
	Kanni._getElementsByClass = function(e) {
		var t = new RegExp("(?:^|\\s)" + e + "(?:$|\\s)");
		var n = document.getElementsByTagName("*");
		var r = [];
		var i;
		for (var s = 0; (i = n[s]) != null; s++) {
			var o = ""+i.className;
			if (o && o.indexOf(e) != -1 && t.test(o))
				r.push(i)
		}
		return r
	};
	Kanni._attachEvent = function(e, t, n) {
		if (document.addEventListener) {
			e.addEventListener(t, n)
		} else {
			e.attachEvent("on" + t, n)
		}
	};
	Kanni.enableNode = function(e) {
		if (typeof e == "string") {
			e = document.getElementById(e)
		}
		if (e.className.match(/\bkanni-enabled-processed\b/)) {
			return
		}
		this._attachEvent(e, "keypress", this.keyPressHandler);
		this._attachEvent(e, "focus", this.showLanguageSwitcher);
		this._attachEvent(e, "blur", this.hideLanguageSwitcher);
		e.className = e.className + " kanni-enabled-processed"
	};
	Kanni._setStyleAttribute = function(e, t, n) {
		if (typeof jQuery != "undefined") {
			jQuery(e).css(t, n);
			return
		}
		var r = e.getAttribute("style");
		if (r) {
			r += ";" + t + ":" + n
		} else {
			r = t + ":" + n
		}
		if (e.setAttribute) {
			e.setAttribute("style", r)
		}
		if (e.style && t in e.style) {
			e.style[t] = r
		}
	};
	Kanni._attachEvent(window, "load", function() {
		Kanni.init()
	})
})()