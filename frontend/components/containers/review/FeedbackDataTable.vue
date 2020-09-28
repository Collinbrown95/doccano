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
      :options.sync="options"
      :server-items-length="totalFeedback"
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
      options: {},
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
  watch: {
    '$route.query': '$fetch',
    options: {
      handler(newvalue, oldvalue) {
        this.$router.push({
          query: {
            limit: this.options.itemsPerPage,
            offset: (this.options.page - 1) * this.options.itemsPerPage,
            q: this.search
          }
        })
      },
      deep: true
    }
  },
  methods: {
    ...mapActions('documents', ['getDocumentFeedbackList', 'getDocumentList', 'updateDocument'])
  }
}
</script>
