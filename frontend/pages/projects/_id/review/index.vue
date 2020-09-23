<template>
  <v-card>
    <v-card-title class="mb-2">
      <h1>REVIEW CONTROLS HERE</h1>
    </v-card-title>
    <feedback-data-table />
  </v-card>
</template>

<script>
import FeedbackDataTable from '@/components/containers/review/FeedbackDataTable'

export default {
  layout: 'project',
  components: {
    FeedbackDataTable
  }
}
</script>
