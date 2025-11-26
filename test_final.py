from compiler import compile

codigo = """
int main() {
    int a = 7;
    int b = 8;
    int r = (a + b) * 2;
    return 0;
}
"""

print("Testando compilador restaurado...")
result = compile(codigo, optimize=True, verbose=False)

if result['success']:
    print("✓ Compilacao bem-sucedida!")
    print(f"  Tokens: {len(result['tokens'])}")
    print(f"  IR: {len(result['ir'].get_instructions())} instrucoes")
    
    if result.get('algebraic_ir'):
        print(f"  IR Algebrico: {len(result['algebraic_ir'].get_instructions())} instrucoes")
    
    print(f"  IR Otimizado: {len(result['optimized_ir'].get_instructions())} instrucoes")
    
    # Verifica shift
    if result.get('assembly'):
        asm_text = '\n'.join(result['assembly']) if isinstance(result['assembly'], list) else result['assembly']
        if 'SHL' in asm_text:
            print("  ✓ SHIFT OPTIMIZATION detectada (a*2 -> a<<1)!")
        else:
            print("  ✗ Shift optimization NAO detectada")
    
    reduction = ((len(result['ir'].get_instructions()) - len(result['optimized_ir'].get_instructions())) / 
                 len(result['ir'].get_instructions()) * 100)
    print(f"  Reducao: {reduction:.1f}%")
else:
    print("✗ ERRO na compilacao!")
    for erro in result['errors']:
        print(f"  - {erro}")
