import logic

if __name__ == '__main__':

    wumpus_kb = logic.PropKB()
    P11, P12, P21, P22, P31,B11, B21 = logic.expr('P11, P12, P21, P22, P31, B11, B21')
    #B100 = logic.expr('B100')
    wumpus_kb.tell(~P11)
    wumpus_kb.tell(B11 | '<=>' | ((P12 | P21)))
    wumpus_kb.tell(B21 | '<=>' | ((P11 | P22 | P31)))
    wumpus_kb.tell(~B11)
    ship = (1,23,4)
    shipstr = 'P'+str((ship[0]+1,ship[1],ship[2]))
    #for v in ship:
     #   shipstr += str(v)
    print(shipstr)
    wumpus_kb.tell(~logic.expr(shipstr))
    result = logic.dpll_satisfiable(logic.to_cnf(logic.associate('&',wumpus_kb.clauses + [logic.expr(P22)])))
    print(result)
    result = logic.dpll_satisfiable(logic.to_cnf(logic.associate('&',wumpus_kb.clauses + [logic.expr(shipstr)])))
    print(result)
