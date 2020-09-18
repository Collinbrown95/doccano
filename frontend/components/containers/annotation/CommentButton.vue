<template>
  <div style="display:inline;">
    <v-tooltip bottom>
      <template v-slot:activator="{ on }">
        <v-btn
          :disabled="disabled"
          class="text-capitalize ps-1 pe-1"
          min-width="36"
          outlined
          v-on="on"
          @click="dialog=true"
        >
          <v-icon>
            mdi-flag-outline
          </v-icon>
        </v-btn>
      </template>
      <span>Feedback</span>
    </v-tooltip>
    <v-dialog
      v-model="dialog"
      width="800"
    >
      <comment-card
        v-if="currentProject"
        :guideline-text="currentProject.guideline"
        @close="dialog=false"
      />
    </v-dialog>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import CommentCard from '@/components/organisms/annotation/CommentCard'
export default {
  components: {
    CommentCard
  },
  props: {
    disabled: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      dialog: false
    }
  },
  computed: {
    ...mapGetters('projects', ['currentProject'])
  }
}
</script>
