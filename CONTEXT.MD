# CONTEXT — Registro de uso de IA

Documentación de los prompts utilizados con asistentes de IA durante el
desarrollo del TPFI, conforme al requisito de la cátedra.

## Herramientas utilizadas

- Asistente de IA conversacional (EcoGPT) para diseño, depuración y revisión.

## Prompts y resultados

### 1. Diseño inicial del servidor proxy

**Prompt:** "Necesito implementar un servidor proxy en Python que use los
patrones Singleton, Observer y Proxy. El servidor recibe JSON por socket TCP
con UUID, ACTION y datos, y debe auditar cada operación en DynamoDB."

**Resultado:** estructura de módulos (`singletonproxyobserver`,
`singletonclient`, `observerclient`) y separación de responsabilidades entre
`handle_client`, `Subject` y las clases de acceso a datos.

### 2. Merge parcial en `set`

**Prompt:** "El `set` actual reemplaza el registro completo. La consigna pide
que los campos no informados conserven el valor anterior o queden en blanco si
el registro es nuevo. ¿Cómo lo implemento?"

**Resultado:** lectura previa del registro, copia de los campos presentes en
`CAMPOS_CORPORATE_DATA` y completado con `""` para los ausentes.

### 3. Nombre de la acción de suscripción

**Prompt:** "El ObserverClient envía `suscribe` pero el servidor espera
`suscribirse`, y la consigna dice `subscribe`. ¿Cuál uso?"

**Resultado:** aceptar las tres variantes en el servidor para mantener
compatibilidad.

### 4. Cierre de sockets colgados

**Prompt:** "Agregué `finally: conn.close()` para evitar sockets colgados, pero
eso cierra el socket del suscriptor. ¿Cómo lo resuelvo?"

**Resultado:** bandera `mantener_abierta`, que se activa solo en el caso
`subscribe`, conservando el cierre garantizado en las demás acciones.

### 5. `ProvisionedThroughputExceededException`

**Prompt:** "Los scans de `CorporateLog` fallan por throughput excedido. La
tabla tiene 7890 filas y no puedo borrar datos porque el profesor la revisa.
¿Qué opciones tengo?"

**Resultado:** `ProjectionExpression` con alias `#u` para el campo reservado
`uuid`, límite de páginas en `mis_logs` y reintentos adaptativos de boto3
(`Config(retries={"max_attempts": 20, "mode": "adaptive"})`).

### 6. Tests de patrones

**Prompt:** "La consigna pide que los tests verifiquen que las clases se
implementan como los patrones requeridos. ¿Cómo testeo Singleton, Observer y
Proxy?"

**Resultado:** `tests/test_patrones.py` con verificación de identidad de
instancias, notificación a múltiples suscriptores y delegación del proxy.

### 7. Configuración de calidad

**Prompt:** "Ruff marca I001, E701, E741 y falta de newline final. ¿Cómo los
resuelvo?"

**Resultado:** `ruff check . --fix` para los auto-corregibles, separación del
`else` en línea propia y renombrado de `l` a `log` en las comprensiones.

## Nota

Todo el código generado con asistencia de IA fue revisado, adaptado y validado
con las herramientas de calidad del proyecto antes de su incorporación.
