# Unreleased

These are the changes that will go out in the next release.

## Added

TPFI started out as a project generated from [Cookiecutter PyPackage](https://github.com/audreyfeldroy/cookiecutter-pypackage) containing:

- Initial scaffold for TPFI.
- `src/tpfi/` package with CLI (Typer + Rich), py.typed marker
- Tests with pytest, coverage across Python 3.12/3.13/3.14
- CI via GitHub Actions: lint (Ruff), type check (ty), test matrix, coverage reporting
- Security scanning: CodeQL analysis for public repositories, Dependabot, and a Zizmor workflow audit
- Docs site with Zensical + mkdocstrings and a GitHub Pages deployment workflow
- Trusted publishing to PyPI with OIDC and build provenance attestation
- `justfile` with dev commands: qa, test, type-check, docs-serve, release
- Issue templates, PR template, contributing guide, code of conduct, security policy
- MIT license, .editorconfig, .gitignore

### Contributors

[@PandaAColor](https://github.com/PandaAColor) (Augusto M.Sol) created TPFI.

# Changelog

Todos los cambios relevantes de este proyecto se documentan en este archivo.
El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/)
y el versionado [SemVer](https://semver.org/lang/es/).

## [Unreleased]

### Added
- Tests de aceptación para las cuatro acciones (`get`, `set`, `list`, `subscribe`).
- Tests que verifican la implementación de los patrones Singleton, Observer y Proxy.
- Configuración de reintentos adaptativos de boto3 para evitar
  `ProvisionedThroughputExceededException` en tablas con capacidad provisionada baja.
- Flag `--retry` parametrizable en `observerclient` (default 30 s).

### Changed
- El `set` realiza merge parcial: los campos no informados conservan el valor
  previo o quedan en blanco si el registro es nuevo.
- El `subscribe` acepta las variantes `subscribe`, `suscribe` y `suscribirse`.
- `mis_logs` limita la cantidad de páginas del scan para reducir carga sobre
  `CorporateLog`.

### Fixed
- El `finally: conn.close()` ya no cierra el socket de los suscriptores
  (se usa una bandera `mantener_abierta`).
- Alias `#u` en `ExpressionAttributeNames` para el campo reservado `uuid`.
- El test de suscripción espera `subscribed` (antes `suscribed`).
- Orden de imports y espaciado PEP8 en los tres módulos principales.

## [1.0.0] - 2026-10-21

### Added
- Implementación inicial del servidor proxy con Singleton, Observer y Proxy.
- `singletonclient` con soporte de `get`, `set` y `list`.
- `observerclient` con reconexión automática cada 30 segundos.
- Auditoría de operaciones en la tabla `CorporateLog`.
- Estructura de proyecto generada con CookieCutter.
- Licencia MIT y documentación con pdoc.
