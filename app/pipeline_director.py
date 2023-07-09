from builder.base_builder import BaseBuilder, Pipeline


class PipelineDirector:
    def __init__(self, builder: BaseBuilder) -> None:
        self.builder = builder

    def construct(self) -> Pipeline:
        self.builder.build_staging()
        self.builder.build_dedup()
        self.builder.build_checks()
        self.builder.build_dimensions()
        self.builder.build_target()
        self.builder.build_extras()
        self.builder.build_cleanup()
        return self.builder.pipeline
