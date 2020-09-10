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
          <v-icon v-if="commented">
            mdi-flag
          </v-icon>
          <v-icon v-else>
            mdi-flag-outline
          </v-icon>
        </v-btn>
      </template>
      <span v-if="commented">Commented</span>
      <span v-else>Not Commented</span>
    </v-tooltip>
    <v-dialog
      v-model="dialog"
      width="800"
    >
      <comment-card
        v-if="currentProject"
        :annotator_comment="annotator_comment"
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
    commented: {
      type: Boolean,
      default: null
    },
    annotator_comment: {
      type: String,
      default: ''
    },
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
