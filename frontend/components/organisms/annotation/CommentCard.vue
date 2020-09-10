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
          v-model="annotator_comment"
          :label="annotator_comment === '' ? 'Describe Issue' : annotator_comment"
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
  props: {
    annotator_comment: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      message: '',
      selectedIssue: {},
      documentIssues: [
        { text: 'Document contains an error', id: 1 },
        { text: 'Document contains null or missing information', id: 2 },
        { text: 'Other error', id: 3 }
      ]
    }
  },
  methods: {
    ...mapActions('documents', ['comment']),
    close() {
      this.$emit('close')
    },
    submit() {
      this.comment({
        projectId: this.$route.params.id,
        issue: this.selectedIssue,
        message: this.message
      })
      this.$emit('close')
    }
  }
}
</script>
