-- CreateTable
CREATE TABLE "events" (
    "id" UUID NOT NULL,
    "event_type" TEXT NOT NULL,
    "source" TEXT NOT NULL,
    "entity_type" TEXT NOT NULL,
    "entityId" UUID NOT NULL,
    "payload" JSONB NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "events_pkey" PRIMARY KEY ("id")
);
