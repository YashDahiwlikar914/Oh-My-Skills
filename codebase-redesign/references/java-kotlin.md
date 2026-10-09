# Java and Kotlin

Covers Maven and Gradle projects, including Spring Boot. For Android, the same package rules apply inside `app/src/main/`.

## Layout

The build tool fixes the outer layout.

```
pom.xml or build.gradle.kts
src/
  main/
    java/ or kotlin/
      com/acme/shop/
        ShopApplication.java
        orders/
        billing/
        shared/
    resources/
      application.yml
      db/migration/
  test/
    java/ or kotlin/
      com/acme/shop/
        orders/
```

## Packages

- Group by feature, as in `com.acme.shop.orders` and `com.acme.shop.billing`. Avoid top-level `controller`, `service` and `repository` packages in a growing app.
- Inside a feature, keep classes flat until the package grows too large. Then split into `web`, `domain` and `persistence` subpackages, or whatever names the repo already uses.
- Make classes package-private when nothing outside the feature uses them. Grouping by feature gives that modifier real power.
- `shared` or `common` holds code two or more features use. Nothing domain-specific.
- For large apps, Gradle or Maven multi-module builds give each domain its own module with enforced boundaries. Propose that only if the user asks for module boundaries.

## Spring Boot

- Keep the `@SpringBootApplication` class in the root package. Component scanning covers that package and everything below it, so beans moved outside it vanish.
- Check `@EntityScan`, `@EnableJpaRepositories` `basePackages` and `@ComponentScan` settings after moves.
- Spring Modulith can verify module boundaries in a test. Offer it and add it only on a yes.

## Naming

- Packages all lowercase, no underscores.
- Java requires a public class to live in a file with the same name. Its folder must match its package for the build to find it.
- Kotlin allows a mismatch between folder and package, but keep them matched.

## Tests

- Tests mirror the main package tree under `src/test/`. Move a test whenever you move its class.
- Test resources go in `src/test/resources/`.
- ArchUnit can enforce package rules in a test. Offer it and add it only on a yes.

## Moving Files Safely

- IntelliJ's Move refactor updates the `package` line, imports and references. Prefer it for Java and Kotlin.
- From the terminal, `git mv`, fix the `package` line, then use the compiler errors as the list of imports to fix.
- Run `./mvnw verify` or `./gradlew build` after each batch.

## Path References to Update

- Fully qualified class names in strings, such as `application.yml` settings, logging config such as `logback.xml` logger names, and reflection
- MyBatis mapper XML `namespace` and `resultType`
- JPA `persistence.xml` and `packagesToScan`
- `META-INF/services` files and Spring `AutoConfiguration.imports`
- Jackson `@JsonTypeInfo` class names stored in JSON, and Java serialization. Moving those classes breaks stored data.
- Build plugin config that names main classes, such as the Spring Boot plugin `mainClass` or the `jar` manifest
- Android `AndroidManifest.xml` activity and service class names, and ProGuard or R8 rules
