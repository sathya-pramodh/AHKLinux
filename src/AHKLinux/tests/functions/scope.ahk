c := 10
func(a, b){
    global c := a + b
}
func(10, 20)
MsgBox % c