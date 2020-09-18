<template>
  <base-card
    title="Report an Issue"
    agree-text="Submit"
    cancel-text="Close"
    @agree="submit"
    @cancel="close"
  >
    <template #content>
      <h2>Describe the issue with the document.</h2>
      <v-form
        ref="form"
      >
        <v-radio-group
          v-model="selectedIssue"
        >
          <v-radio
            v-for="(format, i) in documentIssues"
            :key="i"
            :label="format.text"
            :value="format"
          />
        </v-radio-group>
        <v-textarea
          v-model="annotatorComment"
          :label="annotatorComment === '' ? 'Describe Issue' : annotatorComment"
          counter
          maxlength="1000"
        />
      </v-form>
    </template>
  </base-card>
</template>

<script>
import { mapActions } from 'vuex'
import 'tui-editor/dist/tui-editor-contents.css'
import 'highlight.js/styles/github.css'
import BaseCard from '@/components/molecules/BaseCard'
import '@/assets/style/editor.css'

export default {
  components: {
    BaseCard
  },
  data() {
    return {
      selectedIssue: {},
      annotatorComment: '',
      documentIssues: [
        { text: 'Mistake found in the document contents', id: 1 },
        { text: 'Document contains null or missing information', id: 2 },
        { text: 'Document contents are irrelevant', id: 3 },
        { text: 'Other feedback', id: 4 }
      ]
    }
  },
  methods: {
    ...mapActions('documents', ['comment']),
    close() {
      this.$emit('close')
    },
    submit() {
      console.log('obj is ', {
        projectId: this.$route.params.id,
        comment: this.annotatorComment,
        issue: this.selectedIssue,
        username: localStorage.getItem('username')
      })
      this.comment({
        projectId: this.$route.params.id,
        issue: this.selectedIssue,
        username: localStorage.getItem('username')
      })
      this.$emit('close')
    }
  }
}
</script>
