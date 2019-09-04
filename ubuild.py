build.packages.install("uranium-plus")
import uranium_plus

build.config.update({"uranium-plus": {"module": "deepmerge"}})

uranium_plus.bootstrap(build)
