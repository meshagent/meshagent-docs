FROM mcr.microsoft.com/dotnet/sdk:7.0 AS builder
RUN dotnet tool install retypeapp --tool-path /bin

WORKDIR /build
COPY . /build
RUN retype build --output .docker-build/

FROM httpd:latest
COPY --from=builder /build/.docker-build/ /usr/local/apache2/htdocs/
