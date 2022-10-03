a := 20
MsgBox % (a * 10 / 10) - 20 + 10
a := [1,2,3]
MsgBox % a[1]
a := [[1,2,3],[4,5,6]]
MsgBox % a[1][1]
a := {"a": 1}
MsgBox % a.a
a := {"a":{"b":1}}
MsgBox % a.a.b
a := "Hello, World!"
MsgBox % a
a := "Hello, "."World!"
MsgBox % a
a := "Hello"
MsgBox % a.", World!"
a := ", World!"
MsgBox % "Hello".a