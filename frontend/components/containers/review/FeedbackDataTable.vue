<template>
  <v-card>
    <v-card-title>
      User Feedback
      <v-spacer />
      <v-text-field
        v-model="search"
        append-icon="mdi-magnify"
        label="Search"
        single-line
        hide-details
      />
    </v-card-title>
    <v-data-table
      :headers="headers"
      :items="feedbackItems"
      :items-per-page="5"
    >
      <template v-slot:item.document_text="{ item }">
        <span class="d-flex d-sm-none">{{ item.document_text | truncate(50) }}</span>
        <span class="d-none d-sm-flex">{{ item.document_text | truncate(200) }}</span>
      </template>
    </v-data-table>
  </v-card>
</template>

<script>
import { mapActions, mapState } from 'vuex'

export default {
  async fetch() {
    await this.getDocumentFeedbackList({
      projectId: this.$route.params.id,
      ...this.$route.query
    })
  },
  data() {
    return {
      search: '',
      headers: [
        { text: 'Username', value: 'user' },
        { text: 'User Feedback', value: 'text' },
        { text: 'Document', value: 'document_text' }
      ]
    }
  },
  computed: {
    ...mapState('documents', ['feedbackItems', 'totalFeedback'])
  },
  methods: {
    ...mapActions('documents', ['getDocumentFeedbackList', 'getDocumentList', 'updateDocument'])
  }
}
</script>
