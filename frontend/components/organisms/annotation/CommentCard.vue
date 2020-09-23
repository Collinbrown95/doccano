<template>
  <base-card
    title="Submit Feedback"
    agree-text="Submit"
    cancel-text="Close"
    @agree="submit"
    @cancel="close"
  >
    <template #content>
      <h2>Enter Feedback Below</h2>
      <v-form>
        <v-textarea
          v-model="userFeedback"
          :label="feedback !== null ? '' : 'Describe issue'"
          maxlength="2000"
        />
      </v-form>
    </template>
  </base-card>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

import BaseCard from '@/components/molecules/BaseCard'
export default {
  components: {
    BaseCard
  },
  props: {
    feedback: {
      type: Object,
      default: null
    }
  },
  computed: {
    userFeedback: {
      get() {
        return this.feedback === null ? '' : this.feedback.text
      },
      set(newInput) {
        const document = this.currentDoc()
        const payload = {
          newInput,
          document
        }
        return this.$store.commit('documents/updateFeedback', payload)
      }
    }
  },
  methods: {
    ...mapGetters('documents', ['currentDoc']),
    ...mapActions('documents', ['submitFeedback']),
    close() {
      this.$emit('close')
    },
    submit() {
      this.submitFeedback({
        projectId: this.$route.params.id,
        text: this.userFeedback
      })
      this.$emit('close')
    }
  }
}
</script>
