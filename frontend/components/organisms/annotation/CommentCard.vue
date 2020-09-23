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
          :label="feedback !== null ? '' : 'Describe issue'"
          v-model="feedback.text"
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
  data() {
    return {
      userFeedback: ''
    }
  },
  computed: {
    ...mapGetters('documents', ['feedback'])
  },
  methods: {
    ...mapActions('documents', ['submitFeedback']),
    close() {
      this.$emit('close')
    },
    submit() {
      console.log('this feedback text is ', this.feedback.text)
      this.submitFeedback({
        projectId: this.$route.params.id,
        text: this.userFeedback
      })
      this.$emit('close')
    }
  }
}
</script>
