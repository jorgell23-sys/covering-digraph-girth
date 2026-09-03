# El menor testigo de cada cintura para rad(n) | f(n)

*(English version: [README.md](README.md))*

Tres números enteros que no habían sido calculados, y un teorema chico que hace
posible calcularlos.

**Todo esto se comprueba en dos segundos:**

```bash
git clone https://github.com/jorgell23-sys/covering-digraph-girth
cd covering-digraph-girth
python verify.py
```

Sin instalar nada. Imprime PASS o FAIL para cada una de las 56 comprobaciones.

---

## De qué se trata, desde cero

Tomemos un número, digamos **234 = 2 × 3² × 13**, y dos funciones clásicas:

- **rad(n)** — el producto de sus primos distintos. `rad(234) = 2 × 3 × 13 = 78`.
- **sigma(n)** — la suma de todos sus divisores. `sigma(234) = 546`.

Y ahora dibujemos un grafo. Los **vértices** son los primos que dividen a `n`.
Hay una **flecha q → p** cuando `p` divide a `sigma(q^e)`, donde `q^e` es la
potencia exacta de `q` en `n`:

```
sigma(2)   = 3            →   flecha 2 → 3
sigma(3²)  = 13           →   flecha 3 → 13
sigma(13)  = 14 = 2 × 7   →   flecha 13 → 2
```

El grafo es un triángulo: `2 → 3 → 13 → 2`. Su ciclo más corto mide 3 — decimos
que su **cintura** es 3. Y 234 es el número más chico de su clase con cintura 3.

La pregunta que este trabajo responde: **¿cuál es el número más chico de
cintura k?**

El conjunto donde todo primo queda cubierto así no es nuevo: para `sigma` son
los *prime-abundant numbers* de Pollack y Pomerance (2012), catalogados en OEIS
como [A175200](https://oeis.org/A175200). Lo que se calcula acá es un invariante
de grafos sobre esa familia.

## Los resultados

| cintura | `sigma` | `sigma*` | `phi*` |
|---:|---:|---:|---:|
| 2 | 6 | 6 | 12 |
| 3 | 234 | 6615 | 66825 |
| 4 | 137214 | 4380453 | **1120454775** |
| 5 | 275900625 | 540765225 | — |
| 6 | **180141399900** | 474549075 | — |
| 7 | — | **4485174218525** | — |

Los tres en negrita estaban **fuera del alcance de cualquier búsqueda por
enumeración**. El último ronda los 4,5 × 10¹².

## Por qué no se podían encontrar, y cómo se encontraron

Los testigos de cintura alta son rarísimos. Hasta 10⁹ con `sigma` hay 4138 de
cintura 2, 1065 de cintura 3, 122 de cintura 4 — y **2** de cintura 5. Los
conteos caen por un factor que además crece. Hallar uno de cintura 6 barriendo
enteros exigiría llegar a unos **10¹³**.

La salida es un teorema chico:

> Si algún `n` tiene cintura `k`, el **menor** de ellos tiene exactamente `k`
> primos distintos, y su grafo es un ciclo dirigido puro de largo `k`.

Entonces, en vez de barrer enteros, se **arman ciclos** con primos chicos y se
elige el más barato. El problema deja de ser el tamaño de `n` y pasa a ser
cuántos primos hay que mirar.

La demostración, con sus límites, está en [RESULT.md](RESULT.md) (en inglés).

## Algo que vale la pena mirar

Con `sigma*`, la sucesión de mínimos **baja** una vez:

```
6,  6615,  4380453,  540765225,  474549075,  4485174218525
                          ↑ más chico que el anterior
```

Los dos números comparten el esqueleto `3² × 5² × 11 × 13`, y toda la diferencia
está en un factor:

| | factor | valor |
|---|---|---:|
| cintura 6 | `7³ × 43` | **14749** |
| cintura 5 | `7⁵` | 16807 |

Cerrar el ciclo de 5 obliga a `7⁵`. Alargarlo a 6 deja entrar un primo nuevo, el
43, **y eso permite bajar el exponente a `7³`**. Agregar un vértice salió más
barato que subir un exponente.

Pasa exactamente una vez entre todos los términos conocidos: es un accidente de
ese primo, no una propiedad de la función.

## Cómo está comprobado

Los dos métodos **no comparten ninguna lógica** — la criba no sabe nada de
ciclos, y la construcción nunca mira un entero que no venga de uno — y coinciden
en todos los términos que ambos alcanzan.

Y hay un control externo: la criba cuenta **5327** elementos hasta 10⁹ sin
contar `n = 1`. Pollack y Pomerance publicaron **5328** contándolo. Coinciden
exactamente. Eso prueba este código contra un resultado con referato, calculado
por gente que nunca lo vio.

## Lo que este trabajo NO afirma

- **No afirma ser nuevo.** Se buscó en OEIS y en cuatro bases bibliográficas y
  no apareció — con un control positivo que sí encuentra los trabajos
  relevantes. *No encontrar no es lo mismo que no existir.* Está detallado en
  [PRIOR_ART.md](PRIOR_ART.md).
- **No afirma que las sucesiones sean infinitas.** Si existe testigo de toda
  cintura es otra pregunta, que no se toca acá.
- **No afirma tener interés matemático.** Eso lo juzga quien lo lea.

## Cómo se produjo

El diseño del sistema y la dirección de la investigación son del autor. Los
resultados matemáticos los produjo un sistema automático (Claude, de Anthropic)
bajo esa dirección. Todos los cálculos se verificaron con dos implementaciones
independientes y se cruzaron contra trabajo publicado. El autor responde por la
corrección de todo lo que hay acá.

## Licencia

Código bajo [MIT](LICENSE); texto y datos bajo
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
