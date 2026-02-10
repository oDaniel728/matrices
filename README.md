# Matrix (Python)

Implementação simples de matrizes numéricas em Python, com suporte a operações básicas e manipulação funcional de valores.

## Recursos

* Criação de matrizes por dimensão, ordem ou identidade
* Acesso por linha e coluna (`m[r][c]`)
* Iteração sobre linhas e valores
* Operações básicas:

  * soma e subtração
  * negação
* Funções utilitárias:

  * verificar se é quadrada
  * verificar se é nula
  * verificar se é identidade
  * contagem de valores
* Métodos funcionais:

  * `fill` (preenchimento por regra)
  * `eval` (transformação por regra)

## Exemplo de uso

```python
m = Matrix.from_type(3, 3, 0)
m[0][0] = 1
m[1][1] = 1
m[2][2] = 1

print(m.is_identity())  # True
```

```python
a = Matrix.from_type(2, 2, 1)
b = Matrix.from_identity(2)

c = a + b
print(c)
```

## Observações

* Aceita apenas valores numéricos (`int` e `float`)
* Matrizes devem ter dimensões compatíveis para operações
* Estrutura focada em simplicidade e experimentação
