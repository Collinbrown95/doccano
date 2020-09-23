<template>
  <v-data-table
    :headers="headers"
    :items="feedback_data"
    :items-per-page="5"
  />
</template>

<script>
export default {
  data() {
    return {
      headers: [
        {
          text: 'Document ID',
          align: 'start',
          value: 'document'
        },
        { text: 'Username', value: 'user' },
        { text: 'User Feedback', value: 'text' }
      ],
      feedback_data: [
        {
          document: 1,
          user: 'John Doe',
          text: 'Document contains an error'
        },
        {
          document: 13,
          user: 'John Doe',
          text: 'Document contents are blank'
        },
        {
          document: 13,
          user: 'Jane Doe',
          text: 'nothing in document'
        },
        {
          document: 122,
          user: 'John Doe',
          text: 'empty'
        },
        {
          document: 123,
          user: 'John Doe',
          text: 'empty'
        },
        {
          document: 124,
          user: 'John Doe',
          text: 'empty'
        },
        {
          document: 391,
          user: 'Henry Doe',
          text: 'i think there is a mistake in paragraph 2'
        },
        {
          document: 400,
          user: 'Jane Doe',
          text: 'document seems unrelated to the others, perhaps it was added by accident?'
        }
      ]
    }
  }
}
</script>
